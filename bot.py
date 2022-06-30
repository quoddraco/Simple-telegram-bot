from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import datetime
import random
import os
import sqlite3

TOKEN = "Your token"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
conn = sqlite3.connect('Data.db')#Связывание базы данных с пользовательскими данными


def log_write(first_name, username, text, dt):#Writing logs about interactions with the bot
    file = open('log.txt', 'at')
    dt_string = dt.strftime("Date: %d/%m/%Y  time: %H:%M:%S ")
    user_date = (" First_name: " + first_name + "  User_name: " + username + "  Message: " + text)
    file.write(dt_string + user_date + "\n")
    file.close()


def pic_dir():#Upload image names for "random" issuance to their users
    name_way_photo = []
    path = r"C:\Users\....\bot\photo\photos"

    filelist = []

    for root, dirs, files in os.walk(path):
        for file in files:
            filelist.append(os.path.join(root, file))
    for name in filelist:
        name_way_photo.append(name)

    return name_way_photo


@dp.message_handler(content_types=["photo"])# Accept pictures from users
async def download_photo(message: types.Message):
    await message.photo[-1].download(destination=r"C:\Users\....\bot\photo\photos")


@dp.message_handler(commands="spam")#The function of sending messages to users
async def get_text_messages(msg: types.Message):
    print(msg)
    admin_id="user_name admin"# user_name admin
    dt = datetime.datetime.now()
    if msg.from_user.username == admin_id and msg.text.lower() == '/spam':
        mess=("Админ: "+"Проверка функции рассылки")
        cur = conn.cursor()
        cur.execute(f'''SELECT id_user FROM user_data''')
        spam_base = cur.fetchall()
        for z in range(len(spam_base)):
            await bot.send_message(spam_base[z][0], mess)
    else:
        await msg.reply('Иди нахер')
    text = msg.text
    first_name = msg.from_user.first_name
    username = msg.from_user.username
    log_write(first_name, username, text, dt)

@dp.message_handler(commands="logs")#Log view function
async def get_text_messages(msg: types.Message):
    print(msg)
    admin_id="user_name admin"
    dt = datetime.datetime.now()
    if msg.from_user.username == admin_id and msg.text.lower() == '/logs':
        doc = open('log.txt', 'rb')
        await msg.answer_document(doc)
    else:
        await msg.reply('Иди нахер')
    text = msg.text
    first_name = msg.from_user.first_name
    username = msg.from_user.username
    log_write(first_name, username, text, dt)

@dp.message_handler(commands="admin")#Admin panel
async def get_text_messages(msg: types.Message):
    print(msg)
    admin_id="quoddraco"
    dt = datetime.datetime.now()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/logs","/spam"]
    keyboard.add(*buttons)
    await msg.answer("Выберите кнопку", reply_markup=keyboard)
    if msg.from_user.username != admin_id and msg.text.lower() == '/admin':
        await msg.reply('Иди нахер')
    text = msg.text
    first_name = msg.from_user.first_name
    username = msg.from_user.username
    log_write(first_name, username, text, dt)

@dp.message_handler(commands="start")#Bot start function
async def start(msg: types.Message):
    dt = datetime.datetime.now()
    text = msg.text

    cur = conn.cursor()
    cur.execute(f'''SELECT * FROM user_data WHERE (id_user="{msg.from_user.id}")''')
    entry = cur.fetchone()
    if entry is None:
        cur.execute(
            f'''INSERT INTO user_data VALUES ('{msg.from_user.id}', '{msg.from_user.first_name}','{msg.from_user.username}')''')
        conn.commit()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Привет"]
    keyboard.add(*buttons)
    await msg.answer("Выберите кнопку", reply_markup=keyboard)

    first_name = msg.from_user.first_name
    username = msg.from_user.username
    log_write(first_name, username, text, dt)


@dp.message_handler(content_types=['text'])#Bot features
async def get_text_messages(msg: types.Message):
    dt = datetime.datetime.now()
    name = msg.from_user.first_name

    print(msg)
    if msg.text.lower() == 'привет':
        mess = ("Привет " + name + "!")
        await msg.answer(mess)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["?", "🌄", "🎧", "📽"]
        keyboard.add(*buttons)
        await msg.answer("Выберите кнопку", reply_markup=keyboard)
        text = msg.text

    elif msg.text.lower() == '?':
        await msg.answer(str(random.randint(0, 10000)))
        text = msg.text

    elif msg.text.lower() == '🌄':
        files = pic_dir()
        name_photo = (files[random.randint(0, len(files) - 1)])
        print(name_photo)
        img = open('%(name_photo)s' % {"name_photo": name_photo}, 'rb')
        await msg.answer_photo(img)
        text = "picture"


    elif msg.text.lower() == '🎧':
        audio = open('Lida.mp3', 'rb')
        await msg.answer_audio(audio)
        text = "audio"

    elif msg.text.lower() == '📽':
        video = open('video_2022-06-20_22-25-41.mp4', 'rb')
        await msg.answer_video(video)
        text = "video"

    elif msg.text.lower() == '/exit':
        await msg.answer("Завершение программы!")
        text = msg.text


    else:
        await msg.answer('Не понимаю, что это значит.')
        text = msg.text

    first_name = msg.from_user.first_name
    username = msg.from_user.username
    log_write(first_name, username, text, dt)


if __name__ == '__main__':
    executor.start_polling(dp)
