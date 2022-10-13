from glob import glob
import telebot
import random
import config
from telebot import *
import requests
import handlers.generator as gen
from telebot.types import ReplyKeyboardMarkup


token = config.BOT_TOKEN
bot = telebot.TeleBot(token)
city_index = None 
price = 0
product = None
captcha_string = None

def paymentChoise(message, purchase):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Кодом", callback_data="code"))
    keyboard.add(types.InlineKeyboardButton("Оплата на карту", callback_data="card"))
    keyboard.add(types.InlineKeyboardButton("Bitcoin", callback_data="btc"))
    keyboard.add(types.InlineKeyboardButton("Litecoin", callback_data="ltc"))
    keyboard.add(types.InlineKeyboardButton("Назад", callback_data="cancel"))

    if(purchase):
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard, text=f"""Чем вы будете оплачивать:""")
        return None

    bot.send_message(chat_id=message.chat.id, reply_markup=keyboard, text=f"""Чем вы будете оплачивать:""")


# * CHATBOT function
@bot.message_handler(commands=['start']) 
def captcha_message(message):
    global captcha_string
    captcha_string = gen.generate_captcha(4)
    bot.send_photo(message.chat.id, open("storage/captcha.png", "rb"), caption='Введите текст с картинки:')
    bot.register_next_step_handler(message, check_captcha)

@bot.message_handler(content_types=["text"])
def check_captcha(message):
    if captcha_string == message.text:
        bot.send_message(message.chat.id, "Поздравляем. Вы верно ввели капчу!")
        startMsg(message)
    else:
        bot.send_message(message.chat.id, "Текст не совпадает. Попробуйте ещё раз")
        captcha_message(message)
        

def startMsg(message):    
    # создаём старт кнопки
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)

    # добавляем города
    cities_list = [types.InlineKeyboardButton(i, callback_data=f"city-{i}") for i in config.CITIES]

    # добавляем остальные пункты меню
    balance = types.InlineKeyboardButton('Баланс (0руб.)', callback_data='balance')
    bots = types.InlineKeyboardButton('Мои боты', callback_data='bots')
    refferal = types.InlineKeyboardButton('Реферальная програма', callback_data='refferal')
    latest = types.InlineKeyboardButton('Последний заказ', callback_data='latest')
    support = types.InlineKeyboardButton('Оператор', url=config.SUPPORT)

    keyboard.add(*cities_list)
    keyboard.add(balance)
    keyboard.add(bots)
    keyboard.add(refferal)
    keyboard.add(latest)
    keyboard.add(support)

    bot.send_message(chat_id=message.chat.id, reply_markup=keyboard, text=f"""Выберите пожалуйста город""")

def payMsg(message):
    global price
    price = message.text
    
    paymentChoise(message, False)


# * HANDLERS
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global city_index
    global price
    global product 

    if call.message:
        if call.data.startswith('city-'):
            # проверка на города
            counter = 0

            # форматируем данные
            msg = call.data.partition('-')[2]
            msg = msg[0:30]
            
            for i in config.CITIES:
                counter += 1
                if msg == i[0:30]:
                    # создаём кнопки товара
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    city_index = config.CITIES.index(i)
                    counter -= 1

                    for x in config.PRODUCTS[city_index]:
                        s = x[::-1]
                        s = s[0:25]
                        s = s[::-1]

                        localPrice = config.PRODUCTS[city_index][x]["price"]
                        keyboard.add(types.InlineKeyboardButton(f"{x}({localPrice}руб.)", callback_data=f"product-{s}"))    
                    
                    if(keyboard.keyboard):
                        # bot.send_message(call.message.chat.id, reply_markup=keyboard, text=f"""Выберите товар""")
                        bot.send_message(call.message.chat.id, reply_markup=keyboard, text=f"""Выберите товар""")
                    else:
                        bot.send_message(call.message.chat.id, reply_markup=keyboard, text=f"""Товар закончился""")

                    return city_index

        if call.data.startswith('product-'):
            # проверка на районы
            msg = call.data.partition('-')[2]


            for i in list(config.PRODUCTS[city_index].keys()):
                #обрезаем 30 символов с конца строки
                s = i[::-1]
                s = s[0:25]
                s = s[::-1]

                # проверяем формат.данные
                if msg == s:
                    # создаём кнопки районов
                    keyboard = telebot.types.InlineKeyboardMarkup()

                    # сохраняем данные глобальных перемен ( для послед.использования )
                    price = config.PRODUCTS[city_index][i]["price"]
                    product = i
                    
                    for x in config.PRODUCTS[city_index][i]["regions"]:
                        keyboard.add(types.InlineKeyboardButton(x, callback_data="region"))
                    
                    keyboard.add(types.InlineKeyboardButton("Назад", callback_data="cancel"))

                    city_index = None
                    bot.send_message(call.message.chat.id, reply_markup=keyboard, text=f"""Выберите регион""")
                    return city_index

        if call.data == "region":
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("Оплатить", callback_data="pay"))
            keyboard.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
            
            bot.send_message(call.message.chat.id, reply_markup=keyboard, text=f"""Заявка №{random.randrange(100, 3000)}
Товар и объем <b>{product}</b>
Оплатите {price} руб.
Для проведения оплаты нажмите на кнопку ОПЛАТИТЬ
У вас есть 2 ЧАСА на оплату, после чего заявка будет отменена автоматически""", parse_mode='html') 

            product = None
            return product

        if call.data == "cancel":
            startMsg(call.message)

        if call.data == "pay":
            paymentChoise(call.message, True)
            
        if call.data == "code":
            bot.send_message(call.message.chat.id, text=f"""Технические работы""") 
            price = 0
            startMsg(call.message)

        if call.data == "card":
            ID = random.randrange(10000, 1000000)

            bot.send_message(call.message.chat.id, f"""✅ ВЫДАННЫЕ РЕКВИЗИТЫ ДЕЙСТВУЮТ 30 МИНУТ
✅ ВЫ ПОТЕРЯЕТЕ ДЕНЬГИ, ЕСЛИ ОПЛАТИТЕ ПОЗЖЕ
✅ ПЕРЕВОДИТЕ ТОЧНУЮ СУММУ. НЕВЕРНАЯ СУММА НЕ БУДЕТ ЗАЧИСЛЕНА.
✅ ОПЛАТА ДОЛЖНА ПРОХОДИТЬ ОДНИМ ПЛАТЕЖОМ.
✅ ПРОБЛЕМЫ С ОПЛАТОЙ? ПИСАТЬ В TELEGRAM : {config.SUPPORT}
Предоставить чек об оплате и
ID: {ID}
✅ С ПРОБЛЕМНОЙ ЗАЯВКОЙ ОБРАЩАЙТЕСЬ НЕ ПОЗДНЕЕ 24 ЧАСОВ С МОМЕНТА ОПЛАТЫ.""")       
            bot.send_message(call.message.chat.id, f"""✅Заявка № {ID}. Переведите на банковскую  карту {price} рублей удобным для вас способом. Важно пополнить ровную сумму.
{config.CARD_NUMBER}
‼️ у вас есть 30 мин на оплату, после чего платёж не будет зачислен
‼️ перевёл неточную сумму - оплатил чужой заказ""")       

            price = 0
            return price

        if call.data == "btc":
            r = requests.get('https://blockchain.info/ticker')
            bitprice = int((r.json()['RUB']['buy']))

            actual = '{:f}'.format(price / bitprice)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Оплатите {actual} BTC на адрес {config.BTC}""")       

        if call.data == "ltc":
            actual = '{:f}'.format(price / 10145)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""Оплатите {actual} LTC на адрес {config.LTC}""")  

        if call.data == 'balance':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Введите сумму на которую вы хотите пополнить баланс')
            bot.register_next_step_handler(call.message, payMsg)
            

        if call.data == "latest":
            bot.send_message(call.message.chat.id, "У вас нет подтвержденных заказов")

        if call.data == "bots":
            bot.send_message(call.message.chat.id, """Ваши боты:
У вас нет ботов!""")
            startMsg(call.message)

        if call.data == "refferal":
            startMsg(call.message)
if __name__ == '__main__':
    bot.infinity_polling()