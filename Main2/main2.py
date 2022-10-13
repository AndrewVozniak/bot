from email import message
import telebot
from telebot import *
from subprocess import Popen
import os
import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
token = os.environ["ADMIN_TOKEN2"]
adminPassword = os.environ['ADMIN_PASSWORD2']
bot = telebot.TeleBot(token)
id_list = []


script = Popen(['python3','./Main2/view2.py']) # python если на Windows | python3 если на Linux

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
    script = Popen(['python3','./Main2/view2.py']) # python если на Windows | python3 если на Linux
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
    card_bt = types.InlineKeyboardButton(text="Изменить карту", callback_data="card")
    btc_bt = types.InlineKeyboardButton(text="Изменить btc кошелёк", callback_data="btc")

    # website_bt = types.InlineKeyboardButton(text="Изменить вебсайт", callback_data="website")
    support_bt = types.InlineKeyboardButton(text="Изменить тех.поддержку", callback_data="support")
    operator_bt = types.InlineKeyboardButton(text="Изменить оператора", callback_data="operator")
    # reviews_bt = types.InlineKeyboardButton(text="Изменить отзывы", callback_data="reviews")
    # work_bt = types.InlineKeyboardButton(text="Изменить работу", callback_data="work")

    token_bt = types.InlineKeyboardButton(text="Изменить токен", callback_data="token")
    password_bt = types.InlineKeyboardButton(text="Изменить пароль", callback_data="password")
    reload_bt = types.InlineKeyboardButton(text="Перезагрузить бота", callback_data="reload")
    env_bt = types.InlineKeyboardButton(text="Перезагрузить ENV", callback_data="env")
    info_bt = types.InlineKeyboardButton(text="Информация", callback_data="information")
    
    keyboard = types.InlineKeyboardMarkup(row_width=2).add(info_bt)
    keyboard.add(card_bt, btc_bt, support_bt, operator_bt, password_bt, reload_bt, env_bt, token_bt)

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
            saveENV('карты', message, "CARD_NUMBER2")
        
        elif message.text.startswith('!btc-'):
            saveENV('btc кошелька', message, "BTC2")

        # elif message.text.startswith('!website-'):
        #     saveENV('сайта', message, "WEBSITE") 

        elif message.text.startswith('!support-'):
            saveENV('сапорта', message, "SUPPORT2") 

        elif message.text.startswith('!operator-'):
            saveENV('оператора', message, "OPERATOR2") 
        
        # elif message.text.startswith('!reviews-'):
        #     saveENV('страницы с отзывами', message, "REVIEWS") 
        
        # elif message.text.startswith('!work-'):
        #     saveENV('работы', message, "WORK") 

        elif message.text.startswith('!token-'):
            saveENV('токена', message, "BOT_TOKEN2")

        elif message.text.startswith('!password-'):
            saveENV('пароля', message, "ADMIN_PASSWORD2")

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

        if call.data == "website":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !website-( Значение )")

        if call.data == "support":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !support-( Значение )")

        if call.data == "operator":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !operator-( Значение )")

        if call.data == "reviews":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !reviews-( Значение )")

        if call.data == "work":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !work-( Значение )")

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
Номер карты - {os.environ['CARD_NUMBER2']}
Номер BTC кошелька - {os.environ['BTC2']}
""", parse_mode="Markdown") 

            bot.send_message(call.message.chat.id, f"""
*Ссылки*
Тех.поддержка - {os.environ['SUPPORT2'].partition('e/')[2]}
Оператор - {os.environ['OPERATOR2'].partition('e/')[2]}
""", parse_mode="Markdown") 

            bot.send_message(call.message.chat.id, f"""
*Системные*
Токен бота - {os.environ['BOT_TOKEN2']}
Токен админки - {os.environ['ADMIN_TOKEN2']}
Пароль от админки - {os.environ['ADMIN_PASSWORD2']}
""", parse_mode="Markdown") 

if __name__ == '__main__':
    bot.infinity_polling()