from Token import token
import os
import telebot
from datetime import datetime, timedelta
import asyncio
# import . from Rewrite_api

bot = telebot.TeleBot(token)
keyboard = telebot.types.ReplyKeyboardMarkup()
needtime = ''

temp_subject = ''


@bot.message_handler(commands=['start', 'help', 'hello'])
def start_message(message):
    bot.send_message(message.chat.id, 'Хай, пупсик')

#-------------------------------------------------------------------#


@bot.message_handler(commands=['newclass'])
def new_subject1(message):
    bot.send_message(message.chat.id, 'Назовите предмет')
    bot.register_next_step_handler(message, new_subject2)


def new_subject2(message):
    global temp_subject
    temp_subject = message.text

    if f'{temp_subject}.txt' in os.listdir('files'):
        bot.send_message(message.chat.id, 'Данный предмет уже есть')
        return 0
    with open(f'files/{temp_subject}.txt', mode='w') as file:
        print('', file=file)

    bot.send_message(
        message.chat.id, f'Предмет "{temp_subject}" добавлен в список')


@bot.message_handler(commands=['im_text'])
def import_info1(message):
    bot.send_message(message.chat.id, 'Назовите предмет')
    bot.register_next_step_handler(message, import_info2)


def import_info2(message):
    global temp_subject
    temp_subject = message.text

    if f'{temp_subject}.txt' not in os.listdir('files'):
        bot.send_message(message.chat.id, 'Данного предмета нет в списке')
        return 0
    bot.send_message(message.chat.id, 'Введите текст для шпоры')
    bot.register_next_step_handler(message, import_info3)


def import_info3(message):
    global temp_subject
    text = message.text

    with open(f'files/{temp_subject}.txt', mode='w') as file:
        print(f'{text}', file=file)

    bot.send_message(message.chat.id, f'Текст сохранен в "{temp_subject}"')


@bot.message_handler(commands=['get_text'])
def get_text1(message):
    bot.send_message(message.chat.id, 'Введите название предмета')
    bot.register_next_step_handler(message, get_text2)


def get_text2(message):
    global temp_subject
    temp_subject = message.text

    if f'{temp_subject}.txt' not in os.listdir('files'):
        bot.send_message(message.chat.id, 'Данного предмета нет в списке')
        return 0
    with open(f'files/{temp_subject}.txt', mode='r') as file:
        text = file.read()

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['delete'])
def delete_subject1(message):
    bot.send_message(message.chat.id, 'Введите название предмета')
    bot.register_next_step_handler(message, delete_subject2)


def delete_subject2(message):
    global temp_subject
    temp_subject = message.text

    os.remove(f'files/{temp_subject}.txt')
    bot.send_message(
        message.chat.id, f'Предмет "{temp_subject}" успешно удален')


#-------------------------------------------------------------------#


@bot.message_handler(commands=['set_timer'])
def set_timer1(message):
    bot.send_message(message.chat.id, 'Введите название предмета')
    bot.register_next_step_handler(message, set_timer2)


def set_timer2(message):
    global temp_subject
    temp_subject = message.text

    bot.send_message(
        message.chat.id, 'Через какое время вам отправить сообщение? \n Вводите в формате чч:мм:cc')
    bot.register_next_step_handler(message, set_timer3)


def set_timer3(message):
    global temp_subject, needtime
    
    time = [int(i) for i in message.text.split(':')]
    time = timedelta(hours=time[0], minutes=time[1], seconds=time[2])
    needtime = datetime.datetime.now() + time
    subject = temp_subject
    print(needtime, subject)

    with open(f'files/{subject}.txt', mode='r') as file:
        text = file.read()

    timer(message, 5, text)


async def timer(message, wait_for, text):
    while True:
        await asyncio.sleep(wait_for)

        if datetime.time.now() == needtime:
            bot.send_message(message.chat_id, text)


@bot.message_handler(func=lambda message: True)
def messages(message):
    bot.send_message(message.chat.id, message.text)
    print(f'{message.chat.username}: {message.text}')


bot.polling()
