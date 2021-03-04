from config import token
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from util import RewriteStates
import os
import aiogram
import datetime
import asyncio

bot = aiogram.Bot(token=token)
dp = aiogram.Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
loop = asyncio.get_event_loop()
state = ''
print(RewriteStates.all())
needtime = datetime.datetime.now()
need_to_send = False
Gmessage = ''

temp_subject = ''


@dp.message_handler(commands=['start', 'help', 'hello'])
async def start_message(msg: aiogram.types.Message):
    global state
    state = dp.current_state(user=msg.from_user.id)
    await bot.send_message(msg.from_user.id, 'Хай, пупсик')

#-------------------------------------------------------------------#


@dp.message_handler(commands=['newclass'])
async def new_subject1(msg: aiogram.types.Message):
    await bot.send_message(msg.from_user.id, 'Назовите предмет')
    await state.set_state(RewriteStates.all()[4])


@dp.message_handler(state=RewriteStates.STATE_NEWCLASS)
async def new_subject2(msg: aiogram.types.Message):
    global temp_subject
    temp_subject = msg.text

    if f'{temp_subject}.txt' in os.listdir('files'):
        await bot.send_message(msg.from_user.id, 'Данный предмет уже есть. Введите новый')
        return 0
    with open(f'files/{temp_subject}.txt', mode='w') as file:
        print('', file=file)

    await bot.send_message(
        msg.from_user.id, f'Предмет "{temp_subject}" добавлен в список')

    await state.reset_state()


@dp.message_handler(commands=['im_text'])
async def import_info1(msg: aiogram.types.Message):
    await bot.send_message(msg.from_user.id, 'Назовите предмет')
    await state.set_state(RewriteStates.all()[2])


@dp.message_handler(state=RewriteStates.STATE_IM_TEXT1)
async def import_info2(msg: aiogram.types.Message):
    global temp_subject
    temp_subject = msg.text

    if f'{temp_subject}.txt' not in os.listdir('files'):
        await bot.send_message(msg.from_user.id, 'Данного предмета нет в списке')
        return 0
    await bot.send_message(msg.from_user.id, 'Введите текст для шпоры')
    await state.set_state(RewriteStates.all()[3])


@dp.message_handler(state=RewriteStates.STATE_IM_TEXT2)
async def import_info3(msg: aiogram.types.Message):
    global temp_subject
    text = msg.text

    with open(f'files/{temp_subject}.txt', mode='w') as file:
        print(f'{text}', file=file)

    await bot.send_message(msg.from_user.id, f'Текст сохранен в "{temp_subject}"')

    await state.reset_state()


@dp.message_handler(commands=['get_text'])
async def get_text1(msg: aiogram.types.Message):
    await bot.send_message(msg.from_user.id, 'Введите название предмета')
    await state.set_state(RewriteStates.all()[1])


@dp.message_handler(state=RewriteStates.STATE_GET_TEXT)
async def get_text2(msg: aiogram.types.Message):
    global temp_subject
    temp_subject = msg.text

    if f'{temp_subject}.txt' not in os.listdir('files'):
        await bot.send_message(msg.from_user.id, 'Данного предмета нет в списке')
        return 0
    with open(f'files/{temp_subject}.txt', mode='r') as file:
        text = file.read()

    await bot.send_message(msg.from_user.id, text)

    await state.reset_state()


@dp.message_handler(commands=['delete'])
async def delete_subject1(msg: aiogram.types.Message):
    await bot.send_message(msg.from_user.id, 'Введите название предмета')
    await state.set_state(RewriteStates.all()[0])


@dp.message_handler(state=RewriteStates.STATE_DELETE)
async def delete_subject2(msg: aiogram.types.Message):
    global temp_subject
    temp_subject = msg.text

    os.remove(f'files/{temp_subject}.txt')
    await bot.send_message(
        msg.from_user.id, f'Предмет "{temp_subject}" успешно удален')

    await state.reset_state()


#-------------------------------------------------------------------#


@dp.message_handler(commands=['set_timer'])
async def set_timer1(msg: aiogram.types.Message):
    await bot.send_message(msg.from_user.id, 'Введите название предмета')
    await state.set_state(RewriteStates.all()[5])


@dp.message_handler(state=RewriteStates.STATE_SET_TIMER1)
async def set_timer2(msg: aiogram.types.Message):
    global temp_subject
    temp_subject = msg.text

    await bot.send_message(
        msg.from_user.id, 'Через какое время вам отправить сообщение? \n Вводите в формате чч:мм:cc')
    await state.set_state(RewriteStates.all()[6])


@dp.message_handler(state=RewriteStates.STATE_SET_TIMER2)
async def set_timer3(msg: aiogram.types.Message):
    global temp_subject, needtime, need_to_send, Gmessage

    time = [int(i) for i in msg.text.split(':')]
    time = datetime.timedelta(hours=time[0], minutes=time[1], seconds=time[2])
    now = datetime.datetime.now()
    needtime = now + time
    print(type(now), type(time), type(needtime))
    print(needtime, temp_subject)

    if f'{temp_subject}.txt' not in os.listdir('files'):
        await bot.send_message(msg.from_user.id, 'Данного предмета нет в списке')
        return 0
    with open(f'files/{temp_subject}.txt', mode='r') as file:
        text = file.read()

    Gmessage = [msg.from_user.id, text]
    need_to_send = True

    await state.reset_state()


@dp.message_handler()
async def echo_message(msg: aiogram.types.Message):
    global state
    state = dp.current_state(user=msg.from_user.id)
    await bot.send_message(msg.from_user.id, msg.text)


async def timer(wait_for):
    global need_to_send, needtime, Gmessage
    while True:
        await asyncio.sleep(wait_for)
        if datetime.datetime.now() >= needtime and need_to_send:
            await bot.send_message(*Gmessage)
            print(*Gmessage)
            need_to_send = False
        else:
            print(datetime.datetime.now())


async def shutdown(dispatcher: aiogram.Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    loop.create_task(timer(5))
    aiogram.executor.start_polling(dp, on_shutdown=shutdown)
