import telebot
from telebot import *
from subprocess import Popen
import os
import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
token = os.environ["ADMIN_TOKEN"]
bot = telebot.TeleBot(token)
isAdmin = 0 


script = Popen(['python','view.py'])

def restartScript():
    global script 
    
    script.kill()
    script = Popen(['python','view.py']) # python если на Windows | python3 если на Linux
    print('restarted')

def saveENV(message, key):
    os.environ[key] = message.text.partition('-')[2]
    dotenv.set_key(dotenv_file, key, os.environ[key])
    restartScript()




def adminScreen(message):
    card_bt = types.InlineKeyboardButton(text="Изменить карту", callback_data="card")
    btc_bt = types.InlineKeyboardButton(text="Изменить btc кошелёк", callback_data="btc")
    ltc_bt = types.InlineKeyboardButton(text="Изменить ltc кошелёк", callback_data="ltc")
    support_bt = types.InlineKeyboardButton(text="Изменить оператора", callback_data="support")
    token_bt = types.InlineKeyboardButton(text="Изменить токен", callback_data="token")
    reload_bt = types.InlineKeyboardButton(text="Перезагрузить бота", callback_data="reload")

    keyboard = types.InlineKeyboardMarkup(row_width=2).add(token_bt)
    keyboard.add(card_bt, btc_bt, ltc_bt, support_bt, reload_bt)

    bot.send_message(message.chat.id, f"""❤️Добро пожаловать
В админку!
""", reply_markup=keyboard)

# CHATBOT
@bot.message_handler(content_types=["text"])
def checkInteger(message):
    global isAdmin

    adminPassword = os.environ['ADMIN_PASSWORD']

    if message.text == adminPassword:
        isAdmin = 1
        adminScreen(message)
        return isAdmin
    
    elif message.text.startswith('!card-') and isAdmin == 1:
        saveENV(message, "CARD_NUMBER")
    
    elif message.text.startswith('!btc-') and isAdmin == 1:
        saveENV(message, "BTC")

    elif message.text.startswith('!ltc-') and isAdmin == 1:
        saveENV(message, "LTC")

    elif message.text.startswith('!support-') and isAdmin == 1:
        saveENV(message, "SUPPORT") 

    elif message.text.startswith('!token-') and isAdmin == 1:
        saveENV(message, "BOT_TOKEN")

    else:
        bot.send_message(message.chat.id, f"""Извини, я стандартный бот, я ничего не умею делать :(""")


@bot.callback_query_handler(func=lambda call: True)
def purchaseScreen(call):
    global isAdmin

    if call.message:
        if call.data == "card" and isAdmin == 1:
            bot.send_message(call.message.chat.id, f"Для изменения напиши !card-( Значение )")
        elif call.data == "token" and isAdmin == 1:
            bot.send_message(call.message.chat.id, f"Для изменения напиши !token-( Значение )")
        elif call.data == "btc" and isAdmin == 1:
            bot.send_message(call.message.chat.id, f"Для изменения напиши !btc-( Значение )")
        elif call.data == "ltc" and isAdmin == 1:
            bot.send_message(call.message.chat.id, f"Для изменения напиши !ltc-( Значение )")
        elif call.data == "support" and isAdmin == 1: 
            bot.send_message(call.message.chat.id, f"Для изменения напиши !support-( Значение )") 
        elif call.data == "operator" and isAdmin == 1:
            restartScript()
            bot.send_message(call.message.chat.id, f"Бот перезагружен.") 

if __name__ == '__main__':
    bot.infinity_polling()