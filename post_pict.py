import random  # импортируем модуль случайных событий
import os  # используем из него модуль для переименования файлов
import shutil  # используем из него модуль для перемещения файлов и переименования
from aiogram.types import InputFile  # импортируем модуль отправки обьектов
from bottoken import admin_ID, channel_ID, TOKEN  # импортируем токен, ID админа и ID канала
from aiogram import Bot
from bottoken import post_interval, post_disp
bot = Bot(TOKEN)


# функция постит рандомную картинку и потом переносит ее в другой каталог
async def post_picture_task():
    source_dir = 'picts'  # название каталога из которого берутся файлы
    random_pict = random.choice(os.listdir(source_dir))  # выбираем случайный файл из каталога picts
    photo = InputFile(f'picts/{random_pict}')  # через класс InputFile
    count_files = str(len(os.listdir(path=source_dir))-1)  # считаем остаток файлов в каталоге
    await bot.send_photo(channel_ID, photo=photo)  # аргументы: ID группы, тип файла на передачу
    shutil.move(f'picts/{random_pict}', 'picts_old')  # перемещаем файл в другой каталог
    if count_files == '0':
        await bot.send_message(admin_ID, text='Это был последний файл. Кина больше не будет!')
    else:
        await bot.send_message(admin_ID, text=f'Отправил фотку. В папке "{source_dir}" осталось {count_files} файлов')


def post_time():  # функция случайного смещения времени поста
    time = post_interval + random.randint(0-post_disp, post_disp)
    return time
