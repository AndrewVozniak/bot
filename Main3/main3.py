from email import message
import telebot
from telebot import *
from subprocess import Popen
import os
import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
token = os.environ["ADMIN_TOKEN3"]
adminPassword = os.environ['ADMIN_PASSWORD3']
bot = telebot.TeleBot(token)
id_list = []


script = Popen(['python','./Main3/view3.py']) # python если на Windows | python3 если на Linux

def checkList(data, list):
    for x in list:
        if int(data) == int(x):
            return 1
        else:
            pass

def parseChatID():
    global id_list
    try:
        with open('./storage/admins.txt', 'r', encoding='utf-8') as file:
            id_list = [f"{x}" for x in file]
            id_list = list(map(lambda s: s.strip(), id_list))
    except: 
        with open('./storage/admins.txt', 'w+', encoding='utf-8') as file:
            id_list = [f"{x}" for x in file]
            id_list = list(map(lambda s: s.strip(), id_list))
    

def saveChatID(message):
    if checkList(message.chat.id, id_list) != 1:      
        with open('./storage/admins.txt', 'w', encoding='utf-8') as file:  
            if bool(id_list) == True:
                for i in id_list:
                    file.write(f"{i}\n")

                file.write(f"{message.chat.id}")
                return True
            else:
                file.write(f"{message.chat.id}")
                return False
    else:
        pass

def restartScript():
    global script 
    
    script.kill()
    script = Popen(['python','./Main3/view3.py']) # python если на Windows | python3 если на Linux
    print('restarted')

def saveENV(action, message, key):
    home_bt = types.InlineKeyboardButton(text="На главную страницу", callback_data="home")
    keyboard = types.InlineKeyboardMarkup().add(home_bt)
    os.environ[key] = message.text.partition('-')[2]
    dotenv.set_key(dotenv_file, key, os.environ[key])
    print(os.environ[key])


    if(key == "ADMIN_PASSWORD"):
        global adminPassword
        bot.send_message(message.chat.id, f"""Данные {action} успешно изменены. 
Текущий пароль от панели администратора - {os.environ[key]}. 
Постарайся не забыть его""", reply_markup=keyboard)
        adminPassword = os.environ[key]
        return adminPassword

    else:
        restartScript()
        bot.send_message(message.chat.id, f"""Данные {action} успешно изменены. 
Текущие - {os.environ[key]}. 
Бот успешно перезагружен!""", reply_markup=keyboard)


def adminScreen(message):
    token_bt = types.InlineKeyboardButton(text="Изменить токен", callback_data="token")
    card_bt = types.InlineKeyboardButton(text="Изменить карту", callback_data="card")
    btc_bt = types.InlineKeyboardButton(text="Изменить btc кошелёк", callback_data="btc")
    ltc_bt = types.InlineKeyboardButton(text="Изменить ltc кошелёк", callback_data="ltc")

    support_bt = types.InlineKeyboardButton(text="Изменить тех.поддержку", callback_data="support")
    contact_spb_bt = types.InlineKeyboardButton(text="Изменить контакты СПБ", callback_data="contact_spb")
    contact_msk_bt = types.InlineKeyboardButton(text="Изменить контакты МСК", callback_data="contact_msk")
    visit_bt = types.InlineKeyboardButton(text="Изменить визитку", callback_data="visit")
    website_bt = types.InlineKeyboardButton(text="Изменить вебсайт", callback_data="website")
    work_spb_bt = types.InlineKeyboardButton(text="Изменить работу СПБ", callback_data="work_spb")
    work_msk_bt = types.InlineKeyboardButton(text="Изменить работу МСК", callback_data="work_msk")
    delivery_spb_bt = types.InlineKeyboardButton(text="Изменить доставку СПБ", callback_data="delivery_spb")
    delivery_msk_bt = types.InlineKeyboardButton(text="Изменить доставку МСК", callback_data="delivery_msk")

    password_bt = types.InlineKeyboardButton(text="Изменить пароль", callback_data="password")
    reload_bt = types.InlineKeyboardButton(text="Перезагрузить бота", callback_data="reload")
    env_bt = types.InlineKeyboardButton(text="Перезагрузить ENV", callback_data="env")
    info_bt = types.InlineKeyboardButton(text="Информация", callback_data="information")
    
    keyboard = types.InlineKeyboardMarkup(row_width=2).add(info_bt)
    keyboard.add(card_bt, btc_bt, ltc_bt, support_bt, contact_spb_bt, contact_msk_bt, visit_bt, website_bt, work_spb_bt, work_msk_bt, delivery_spb_bt, delivery_msk_bt, password_bt, reload_bt, env_bt, token_bt)

    bot.send_message(message.chat.id, f"""*❤️ Добро пожаловать в админку! ❤️*
""", parse_mode="Markdown", reply_markup=keyboard)

# CHATBOT
@bot.message_handler(content_types=["text"])
def checkUser(message):
    global id_list
    parseChatID()
    # Проверяем наличие id пользователя в admins.txt. Если он есть даем стартовое сообщение, иначе пользователь должен ввести пароль 
    if checkList(message.chat.id, id_list) == 1:
        saveData(message)
    elif message.text == adminPassword:
        saveChatID(message)
        adminScreen(message)
    else:
        bot.send_message(message.chat.id, f"""Извини, я стандартный бот, я ничего не умею делать :(""")


def saveData(message):
    global id_list
    parseChatID()
    # Проверяем наличие id пользователя в admins.txt. Если он есть даем доступ к командам, иначе пользователь должен ввести пароль 
    if checkList(message.chat.id, id_list) == 1:
        if message.text.startswith('!card-'):
            saveENV('карты', message, "CARD_NUMBER3")
        
        elif message.text.startswith('!btc-'):
            saveENV('btc кошелька', message, "BTC3")

        elif message.text.startswith('!ltc-'):
            saveENV('btc кошелька', message, "LTC3")

        elif message.text.startswith('!support-'):
            saveENV('сапорта', message, "SUPPORT3") 

        elif message.text.startswith('!contact_spb-'):
            saveENV('оператора', message, "CONTACT_SPB3") 

        elif message.text.startswith('!contact_msk-'):
            saveENV('оператора', message, "CONTACT_MSK3") 

        elif message.text.startswith('!visit-'):
            saveENV('оператора', message, "VISIT3") 

        elif message.text.startswith('!website-'):
            saveENV('оператора', message, "WEBSITE3") 

        elif message.text.startswith('!work_spb-'):
            saveENV('оператора', message, "WORK_SPB3") 

        elif message.text.startswith('!work_msk-'):
            saveENV('оператора', message, "WORK_MSK3") 

        elif message.text.startswith('!delivery_spb-'):
            saveENV('оператора', message, "DELIVERY_SPB3") 

        elif message.text.startswith('!delivery_msk-'):
            saveENV('оператора', message, "DELIVERY_MSK3") 

        elif message.text.startswith('!token-'):
            saveENV('оператора', message, "BOT_TOKEN3") 

        elif message.text.startswith('!password-'):
            saveENV('пароля', message, "ADMIN_PASSWORD3")

        else:
            adminScreen(message)

    else:
        bot.send_message(message.chat.id, f"""Извини, я стандартный бот, я ничего не умею делать :(""")


@bot.callback_query_handler(func=lambda call: True)
def purchaseScreen(call):
    if call.message:
        if call.data == "home":
            adminScreen(call.message)

        if call.data == "card":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !card-( Значение )")

        if call.data == "btc":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !btc-( Значение )")

        if call.data == "ltc":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !ltc-( Значение )")

        if call.data == "support":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !support-( Значение )")

        if call.data == "contact_spb":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !contact_spb-( Значение )")

        if call.data == "contact_msk":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !contact_msk-( Значение )")

        if call.data == "website":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !website-( Значение )")

        if call.data == "visit":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !visit-( Значение )")

        if call.data == "work_spb":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !work_spb-( Значение )")

        if call.data == "work_msk":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !work_msk-( Значение )")

        if call.data == "delivery_spb":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !delivery_spb-( Значение )")

        if call.data == "delivery_msk":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !delivery_msk-( Значение )")

        if call.data == "token":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !token-( Значение )")

        if call.data == "password":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !password-( Значение )")

        
        if call.data == "env":
            global dotenv_file

            dotenv_file = dotenv.find_dotenv()
            dotenv.load_dotenv(dotenv_file)            
            restartScript()
            bot.send_message(call.message.chat.id, f"ENV обновлено.") 
            return dotenv_file

        if call.data == "reload":
            restartScript()
            bot.send_message(call.message.chat.id, f"Бот перезагружен.") 


        if call.data == "information":
            bot.send_message(call.message.chat.id, f"""*Текущая информация:*

*Платежные системы*
Номер карты - {os.environ['CARD_NUMBER3']}
Номер BTC кошелька - {os.environ['BTC3']}
Номер LTC кошелька - {os.environ['LTC3']}
""", parse_mode="Markdown") 

            bot.send_message(call.message.chat.id, f"""
Ссылки
Тех.поддержка - {os.environ['SUPPORT3']}
Контакты СПБ - {os.environ['CONTACT_SPB3']}
Контакты МСК - {os.environ['CONTACT_MSK3']}
Визитка - {os.environ['VISIT3']}
Сайт - {os.environ['WEBSITE3']}
Работа СПБ - {os.environ['WORK_SPB3']}
Работа МСК - {os.environ['WORK_MSK3']}
Доставка СПБ - {os.environ['DELIVERY_SPB3']}
Доставка МСК - {os.environ['DELIVERY_MSK3']}
""") 

            bot.send_message(call.message.chat.id, f"""
*Системные*
Токен бота - {os.environ['BOT_TOKEN3']}
Токен админки - {os.environ['ADMIN_TOKEN3']}
Пароль от админки - {os.environ['ADMIN_PASSWORD3']}
""", parse_mode="Markdown") 

if __name__ == '__main__':
    bot.infinity_polling()