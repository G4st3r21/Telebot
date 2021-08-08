from data.config import token, founder_id
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from data.Meduza_API import NewsFromMeduza
from data.weather_API import WeatherCheck
from data.dialog_module import AI_chatting
from data.db import UsersTable, ReminderTable
from data import Sticers as sticers
import data.keyboard as kb
import os
import aiogram
from datetime import datetime as dt
import asyncio
import logging


# ----------------------bot init------------------------ #

bot = aiogram.Bot(token=token)
dp = aiogram.Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
loop = asyncio.get_event_loop()
logging.basicConfig(filename='logs.txt', encoding='utf-8', level=logging.INFO)
logging.info('Я запустився')

path = os.path.abspath('data/Answers/tardis-isbv-a8b739ce96e6.json')
print(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
print(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# --------------------other params----------------------- #

state = ''

weekdays = {
    1: 'Понедельник',
    2: 'Вторник',
    3: 'Среда',
    4: 'Четверг',
    5: 'Пятница',
    6: 'Суббота',
    7: 'Воскресенье'
}

months = {
    1: 'Января',
    2: 'Февраля',
    3: 'Марта',
    4: 'Апреля',
    5: 'Мая',
    6: 'Июня',
    7: 'Июля',
    8: 'Августа',
    9: 'Сентября',
    10: 'Октября',
    11: 'Ноября',
    12: 'Декабря',
}

# ----------------------Стартовые сообщения------------------------ #


@dp.message_handler(commands=['start', 'hello'])
async def start_message(msg: aiogram.types.Message):
    global state
    state = dp.current_state(user=msg.from_user.id)
    await bot.send_sticker(msg.from_user.id, sticers.def_s)
    await bot.send_message(msg.from_user.id, 'Хай! Я Тардис, машина времени. Ну почти...', reply_markup=kb.greet_kb)
    UsersTable.add_to_db((msg.from_user.username, msg.from_user.id))


@dp.message_handler(commands=['help'])
async def help_message(msg: aiogram.types.Message):
    with open(f'data/Answers/HELP.txt', mode='r', encoding='utf-8') as file:
        text = file.read()
    await bot.send_sticker(msg.from_user.id, sticers.def_s)
    await bot.send_message(msg.from_user.id, text)
    print(f'{msg.from_user.username}: /help')

#-----------------------------Для Разработчика--------------------------------#

@dp.message_handler(commands=['db'])
async def return_db(msg: aiogram.types.Message):
    await bot.send_document(msg.from_user.id, ('AllTables.db', 'db/AllTables.db'))

#-----------------------------Функционал--------------------------------#

@dp.message_handler(commands=['weather'])
async def weatherNow(msg: aiogram.types.Message):
    data = WeatherCheck()
    await bot.send_message(msg.from_user.id, ''.join(data))


@dp.message_handler(commands=['news'])
async def newsNow(msg: aiogram.types.Message):
    data = NewsFromMeduza(7)
    await bot.send_message(msg.from_user.id, '\n\n'.join(data), parse_mode='HTML')

async def ReminderON():
    while True:
        asyncio.wait_for(1)

        rem = ReminderTable()
        time = str(dt.now())[:16]
        people = rem.check_avaibility(time)
        if people:
            for i in people:
                text, id = f'Напоминаю:\n{i[0]}', i[2]
                rem.del_from_db(text)
                await bot.send_message(id, text)

#-----------------------Текстовые команды--------------------------#

@dp.message_handler()
async def text_comands(msg: aiogram.types.Message):
    text = (str(msg.text).strip()).lower()
    logging.info(f'{msg.from_user.username}: {text}')
    if text == 'время':
        await bot.send_message(msg.from_user.id, f'Сейчас {str(dt.now())[11:19]}')
    elif text == 'погода':
        await weatherNow(msg)
    elif text == 'новости':
        await newsNow(msg)
    elif text == 'привет':
        await start_message(msg)
    elif text == 'логи':
        if msg.from_user.id == founder_id:
            with open('logs.txt', 'r', encoding='utf-8') as file:
                logs = file.readlines()[-1:-15:-1]
                logging.warning('Логи выданы разработчику')
                await bot.send_message(msg.from_user.id, ''.join(logs))
        else:
            logging.warning(f'{msg.from_user.username} запросил логи. Отказано в доступе.')
            await bot.send_message(msg.from_user.id, f'У вас недостаточно прав, я не могу поделиться логами с вами(')
    else:
        ans = AI_chatting(text)
        if ans:
            logging.info(f'Мой ответ: "{ans}"')
            await bot.send_message(msg.from_user.id, ans)
        else:
            logging.warning('Я не нашел ответа на это сообщение :(')
            print('Я не нашел ответ на сообщения пользователя', {msg.from_user.username}, 'см. логи')
            await bot.send_message(msg.from_user.id, 'Я конечно искуственный интеллект, но на это отвечать еще не научился(')

#-----------------------------Разное--------------------------------#

@dp.message_handler(commands=['problem'])
async def Day_with_problem(msg: aiogram.types.Message):
    daysWithoutProblems = 0

@dp.message_handler()
async def def_message(msg: aiogram.types.Message):
    global state
    state = dp.current_state(user=msg.from_user.id)
    # await bot.send_sticker(msg.from_user.id, sticers)
    await bot.send_message(msg.from_user.id, 'Я не знаю, как на это реагировать\nЕсть вопросы? Напиши - /help!')
    print(f'{msg.from_user.username}: {msg.text}')

async def shutdown(dispatcher: aiogram.Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    # loop.create_task(news_every_need_time())
    loop.create_task(ReminderON())
    aiogram.executor.start_polling(dp, on_shutdown=shutdown)
