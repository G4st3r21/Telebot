from data.config import token, founder_id
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from data.Meduza_API import NewsFromMeduza
from data.db import UsersTable, TaskTable
from data import Sticers
import os
import aiogram
from datetime import datetime as dt
import asyncio
from data import Sticers


# ----------------------bot init------------------------ #

bot = aiogram.Bot(token=token)
dp = aiogram.Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
loop = asyncio.get_event_loop()

# --------------------other params----------------------- #

state = ''
needtime = dt.now()
need_to_send = False
Gmessage = ''
daysWithoutProblems = 0

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
    await bot.send_sticker(msg.from_user.id, Sticers.def_morshu)
    await bot.send_message(msg.from_user.id, 'Хай! Я Моршу, твой верный слуга)')
    UsersTable.add_to_db((msg.from_user.username, msg.from_user.id))
    print(f'{msg.from_user.username}: /hello')


@dp.message_handler(commands=['help'])
async def help_message(msg: aiogram.types.Message):
    with open(f'files/HELP.txt', mode='r', encoding='utf-8') as file:
        text = file.read()
    await bot.send_sticker(msg.from_user.id, Sticers.help_morshu)
    await bot.send_message(msg.from_user.id, text)
    print(f'{msg.from_user.username}: /help')

#--------------------------Новости на каждое утро----------------------------#

@dp.message_handler(commands=['testms'])
async def Morning_Mailing(msg: aiogram.types.Message):
    with open('data/morning_text.txt', 'r', encoding='utf-8') as text:
        text = text.readlines()
    news = NewsFromMeduza(10)
    # print(*text)

    for i in range(len(text)):
        # print(text[i])
        if '[ДАТА УДАЛЕНА]' in text[i]:
            today = str(dt.today())[:11].split('-')
            today[1] = months[int(today[1])].lower()
            today[0] = weekdays[int(dt.today().isoweekday())].lower()
            today.reverse()
            text[i] = text[i].replace('[ДАТА УДАЛЕНА]', str(''.join(today[:-1]) + f' - {today[-1]}'))
            # print(today, text[i])
        elif '[ДПБП УДАЛЕНО]' in text[i]:
            text[i] = text[i].replace('[ДПБП УДАЛЕНО]', str(daysWithoutProblems))
        elif '[ПОГОДА УДАЛЕНА]' in text[i]:
            text[i] = text[i].replace('[ПОГОДА УДАЛЕНА]', '[В РАЗРАБОТКЕ]')
        elif '[НОВОСТИ УДАЛЕНЫ]' in text[i]:
            text[i] = text[i].replace('[НОВОСТИ УДАЛЕНЫ]', '\n\n'.join(news))
    
    await bot.send_message(msg.from_user.id, ''.join(text), parse_mode='HTML')
    print(f'{msg.from_user.username}: testing news...')


@dp.message_handler(commands=['news'])
async def news_every_day(msg: aiogram.types.Message):
    data = NewsFromMeduza(7)
    await bot.send_message(msg.from_user.id, '\n\n'.join(data), parse_mode='HTML')
    print(f'{msg.from_user.username}: /news')


@dp.message_handler(commands=['news_enable'])
async def news_enable(msg: aiogram.types.Message):
    WantNews = UsersTable.check_info_by_id(msg.from_user.id)
    if WantNews[-1]:
        await bot.send_message(msg.from_user.id, 'Вы и так подписаны на рассылку)')
    else:
        UsersTable.want_to_see_news(msg.from_user.id, 1)
        await bot.send_message(msg.from_user.id, 'Вы успешно подписались на рассылку новостей!\nЯ отправляю новости в 7:20 каждого дня)')
    print(f'{msg.from_user.username}: /news_enable')


@dp.message_handler(commands=['news_disable'])
async def news_disable(msg: aiogram.types.Message):
    WantNews = UsersTable.check_info_by_id(msg.from_user.id)
    if WantNews[-1]:
        UsersTable.want_to_see_news(msg.from_user.id, 0)
        await bot.send_message(msg.from_user.id, 'Вы успешно отписались(')
    else:
        await bot.send_message(msg.from_user.id, 'Вы и так не подписаны(')
    print(f'{msg.from_user.username}: /news_disable')


async def news_every_need_time():
    users = UsersTable.check_Want_News()

    if str(dt.now())[11:16] == '04:20':
        news = NewsFromMeduza(5)
        for user in users:
            await bot.send_sticker(user[2], Sticers.def_morshu)
            await bot.send_message(user[2], '\n\n'.join(news), parse_mode='HTML')

    await asyncio.sleep(60)

#-----------------------------Разное--------------------------------#


@dp.message_handler()
async def def_message(msg: aiogram.types.Message):
    global state
    state = dp.current_state(user=msg.from_user.id)
    await bot.send_sticker(msg.from_user.id, Sticers.excausted_morshu)
    await bot.send_message(msg.from_user.id, 'Я не знаю, как на это реагировать\nЕсть вопросы? Напиши - /help!')
    print(f'{msg.from_user.username}: {msg.text}')


async def timer(wait_for):
    global need_to_send, needtime, Gmessage
    while True:
        await asyncio.sleep(wait_for)

        if dt.now() >= needtime and need_to_send:
            await bot.send_message(*Gmessage)
            print(*Gmessage)
            need_to_send = False

        # new_post = Check_for_new_post()
        # if new_post:
        #     await bot.send_message(founder_id, new_post, parse_mode='HTML')


async def shutdown(dispatcher: aiogram.Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    loop.create_task(timer(5))
    loop.create_task(news_every_need_time())
    aiogram.executor.start_polling(dp, on_shutdown=shutdown)
