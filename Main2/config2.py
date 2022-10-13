import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = "murbot"
BOT_TOKEN = os.getenv("BOT_TOKEN2")
CARD_NUMBER = os.getenv("CARD_NUMBER2")
BTC = os.getenv("BTC2")
OPERATOR = os.getenv("OPERATOR2")
SUPPORT = os.getenv("SUPPORT2")



CITIES = ["Казань", "Зеленодольск", "Чистополь", "Волжск"]

PRODUCTS = [
    # Казань
    {
        "🙀Мефедрон White🙀 1,5г ": {"price": 6750,"regions": ["Вахитовский", "Кировский", "Московский", "Ново-Савиновский", "Приволжский", "Советский"],},
        "🙀Мефедрон White🙀 1г ": {"price": 4500,"regions": ["Авиастроительный", "Вахитовский", "Кировский", "Московский", "Ново-Савиновский", "Приволжский", "Советский"],},
        "🌲Шишка Devil🌲 1г": {"price": 3000,"regions": ["Авиастроительный", "Вахитовский", "Кировский", "Московский", "Ново-Савиновский", "Приволжский", "Советский"],},
        "🌲Шишка Devil🌲 2г": {"price": 5050,"regions": ["Авиастроительный", "Приволжский", "Советский"],},
        "🌪AMF(Амфетамин)1г ": {"price": 2900,"regions": ["Авиастроительный", "Вахитовский", "Кировский", "Московский", "Ново-Савиновский", "Приволжский", "Советский",],},
        "🙀Мефедрон White🙀 1, 5г ": {"price": 6850,"regions": ["Кировский"],},
        "🍫Гаш(black) 2г ": {"price": 5000,"regions": ["Авиастроительный", "Вахитовский", "Московский", "Ново-Савиновский", "Приволжский"],},
        "🍫Гаш(black) 1г": {"price": 3050,"regions": ["Авиастроительный", "Ново-Савиновский", "Приволжский", "Советский"],},
        "🍭Таблы Chupa_Chups🍭-2шт ": {"price": 3000,"regions": ["Авиастроительный", "Вахитовский", "Кировский", "Московский", "Ново-Савиновский", "Приволжский", "Советский"],},
        "🔃6IX9NINE экстази 2ш ": {"price": 3000,"regions": ["Авиастроительный", "Вахитовский", "Кировский", "Московский", "Ново-Савиновский", "Приволжский", "Советский"],},
        "🟦Emerald Cryss(A-pvp)1г ": {"price": 4000,"regions": ["Авиастроительный", "Кировский", "Московский", "Приволжский"],},
    },

    # Зеленодольск
    { 
        "🙀Мефедрон White🙀 1,5г ": {"price": 6580,"regions": ["Город"],},
        "🍭Таблы Chupa_Chups🍭-2шт ": {"price": 3100,"regions": ["Город"],},
    },

    # Чистополь
    {
        "🟡Amber Cryss (A-pvp) 1г": {"price": 4000,"regions": ["Советский"],},
    },


    # Волжск
    {
        "🙀Мефедрон White🙀 1,5г ": {"price": 6950,"regions": ["Город"],},
        "🙀Мефедрон White🙀 1,5г ": {"price": 6950,"regions": ["Город"],},
        "🌪AMF(Амфетамин)1г ": {"price": 3000,"regions": ["Город",],},
        "🙀Мефедрон White🙀 1г ": {"price": 4600,"regions": ["Город"],},
    },
]

# list(PRODUCTS[0].keys())[0]

# print(PRODUCTS[0]["💎Мефедрон (кристал белоснежный)15г(58400руб.)"]["regions"])

# 🌆Култук🌆", "🌆Свирск🌆", "🌆Баяндай🌆", "🌆Еланцы🌆", "🌆Большая Речка🌆", "🌆Новая Игирма🌆", "🌆Бохан🌆", "🌆Бирюсинск🌆", "🌆Алзамай🌆", "🌆Утулик🌆", "🌆Залари🌆", "🌆Кутулик🌆", "🌆Карлук🌆", "🌆Качуг🌆", "🌆Жигалагово🌆", "🌄Мальта🌄                       
# ❤️💜💚🤎☘️🖤🟢⚫️⬛️🟡🔶💊🍋🚘🍪🌈🧲💼||||||||||||||||||||||||| 🏘🏭🌟🌝☀️🚢🌃🌁🏛🏡🛤 🏜🗻🏣🏠🚏🛸❄️⭐️🏔 🍫⚪️