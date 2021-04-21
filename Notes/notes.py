import aiogram
from .data.util import RewriteStates
from .main import dp, bot, state

#------------------------Работа с информацией------------------------#

@dp.message_handler(commands=['newclass'])
async def new_subject1(msg: aiogram.types.Message):
    await bot.send_message(msg.from_user.id, 'Назовите новое хранилище')
    await state.set_state(RewriteStates.all()[4])
    print(f'{msg.from_user.username}: /newclass')


@dp.message_handler(state=RewriteStates.STATE_NEWCLASS)
async def new_subject2(msg: aiogram.types.Message):
    global temp_subject
    temp_subject = msg.text

    if f'{temp_subject}.txt' in os.listdir('files'):
        await bot.send_message(msg.from_user.id, 'Данное хранилище уже есть. Введите новое')
        return 0
    with open(f'files/{temp_subject}.txt', mode='w') as file:
        print('', file=file)

    await bot.send_message(
        msg.from_user.id, f'Хранилище "{temp_subject}" создано')

    print(os.listdir('files/'))

    await state.reset_state()
    print(f'{msg.from_user.username}: создал хранилище "{temp_subject}"')


@dp.message_handler(commands=['im_text'])
async def import_info1(msg: aiogram.types.Message):
    await bot.send_message(msg.from_user.id, 'Назовите хранилище')
    await state.set_state(RewriteStates.all()[2])
    print(f'{msg.from_user.username}: /im_text')


@dp.message_handler(state=RewriteStates.STATE_IM_TEXT1)
async def import_info2(msg: aiogram.types.Message):
    global temp_subject
    temp_subject = msg.text

    if temp_subject == 'HELP':
        await bot.send_message(
            msg.from_user.id, 'НЕВОЗМОЖНО')
        await state.reset_state()
        return 0

    if f'{temp_subject}.txt' not in os.listdir('files'):
        await bot.send_message(msg.from_user.id, 'Данного хранилища нет в списке')
        return 0
    await bot.send_message(msg.from_user.id, 'Введите текст для хранилища')
    await state.set_state(RewriteStates.all()[3])


@dp.message_handler(state=RewriteStates.STATE_IM_TEXT2)
async def import_info3(msg: aiogram.types.Message):
    global temp_subject
    text = msg.text

    with open(f'files/{temp_subject}.txt', mode='w') as file:
        print(f'{text}', file=file)

    await bot.send_message(msg.from_user.id, f'Текст сохранен в "{temp_subject}"')

    await state.reset_state()
    print(f'{msg.from_user.username}: изменил информацию в {temp_subject}')


@dp.message_handler(commands=['get_text'])
async def get_text1(msg: aiogram.types.Message):
    await bot.send_message(msg.from_user.id, 'Введите название хранилища')
    await state.set_state(RewriteStates.all()[1])
    print(f'{msg.from_user.username}: /get_text')


@dp.message_handler(state=RewriteStates.STATE_GET_TEXT)
async def get_text2(msg: aiogram.types.Message):
    global temp_subject
    temp_subject = msg.text

    if f'{temp_subject}.txt' not in os.listdir('files'):
        await bot.send_message(msg.from_user.id, 'Данного хранилища нет в списке')
        return 0
    with open(f'files/{temp_subject}.txt', mode='r', encoding='utf-8') as file:
        text = file.read()

    await bot.send_message(msg.from_user.id, text)

    await state.reset_state()
    print(f'{msg.from_user.username}: получил текст из "{temp_subject}"')


@dp.message_handler(commands=['delete'])
async def delete_subject1(msg: aiogram.types.Message):
    await bot.send_message(msg.from_user.id, 'Введите название хранилища')
    await state.set_state(RewriteStates.all()[0])
    print(f'{msg.from_user.username}: /delete')


@dp.message_handler(state=RewriteStates.STATE_DELETE)
async def delete_subject2(msg: aiogram.types.Message):
    global temp_subject
    temp_subject = msg.text

    if temp_subject == 'HELP':
        await bot.send_message(
            msg.from_user.id, 'НЕВОЗМОЖНО')
        await state.reset_state()
        return 0

    os.remove(f'files/{temp_subject}.txt')
    await bot.send_message(
        msg.from_user.id, f'Хранилище "{temp_subject}" успешно удалено')

    print(os.listdir('files/'))
    print(f'{msg.from_user.username}: удалил хранилище {temp_subject}')

    await state.reset_state()


@dp.message_handler(commands=['set_timer'])
async def set_timer1(msg: aiogram.types.Message):
    await bot.send_message(msg.from_user.id, 'Введите название хранилища')
    await state.set_state(RewriteStates.all()[5])
    print(f'{msg.from_user.username}: /set_timer')


@dp.message_handler(state=RewriteStates.STATE_SET_TIMER1)
async def set_timer2(msg: aiogram.types.Message):
    global temp_subject
    temp_subject = msg.text

    if f'{temp_subject}.txt' not in os.listdir('files'):
        await bot.send_message(msg.from_user.id, 'Данного хранилища нет в списке')
        await state.reset_state()
        return 0

    await bot.send_message(
        msg.from_user.id, 'Через какое время вам отправить текст?\nВводите в формате чч:мм:cc')
    await state.set_state(RewriteStates.all()[6])


@dp.message_handler(state=RewriteStates.STATE_SET_TIMER2)
async def set_timer3(msg: aiogram.types.Message):
    global temp_subject, needtime, need_to_send, Gmessage

    try:
        time = [int(i) for i in msg.text.split(':')]
        time = dt.timedelta(
            hours=time[0], minutes=time[1], seconds=time[2])
        now = dt.now()
        needtime = now + time
    except Exception:
        await bot.send_message(msg.from_user.id, 'Ошибка: неверный формат, вводите в формате чч:мм:cc')
    print(type(now), type(time), type(needtime))
    print(needtime, temp_subject)

    with open(f'files/{temp_subject}.txt', mode='r', encoding='utf-8') as file:
        text = file.read()

    Gmessage = [msg.from_user.id, text]
    need_to_send = True

    await bot.send_message(msg.from_user.id, 'Хорошо, ожидайте)')
    print(f'{msg.from_user.username}: запустил таймер')
    await state.reset_state()

