from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_hi = KeyboardButton('Привет')
button_weather = KeyboardButton('Погода')
button_news = KeyboardButton('Новости')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_hi)
greet_kb.add(button_weather)
greet_kb.add(button_news)
