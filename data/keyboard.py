from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# DEFAULT

button_hi = KeyboardButton('Привет')
button_weather = KeyboardButton('Погода')
button_news = KeyboardButton('Новости')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_hi)
greet_kb.add(button_weather)
greet_kb.add(button_news)


# MAILING

button_yes = KeyboardButton('1')
button_no = KeyboardButton('2')

mailing_kb = ReplyKeyboardMarkup(resize_keyboard=True)
mailing_kb.add(button_yes)
mailing_kb.add(button_no)

inline_btn_mailing_1 = InlineKeyboardButton('Хочу предложить идею!', callback_data='button_yes')
inline_btn_mailing_2 = InlineKeyboardButton('Может, в другой раз', callback_data='button_no')

inline_maling = InlineKeyboardMarkup(row_width=1).add(inline_btn_mailing_1, inline_btn_mailing_2)
