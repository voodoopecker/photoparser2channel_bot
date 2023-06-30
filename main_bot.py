from aiogram import Bot, Dispatcher, types, executor
from bottoken import TOKEN, admin_ID, channel_ID  # импортируем токен, ID админа, ID канала, переменную интервала запуска планировщика
import keyboard  # импортируем клавиатуру
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # импортируем модуль планировщика
from post_pict import post_picture_task  # импортируем функцию постинга
from parser_pict import pars_pictures_task  # импортируем функцию парсинга
from post_pict import post_time  # импортируем время постинга для планировщика
from compare_pict import compare_pictures_task  # импортируем функцию удаления дублей
import requests  # импортируем модуль для использования get запросов
import os  # импортируем модуль для работы с файлами


bot = Bot(TOKEN)
dp = Dispatcher(bot)
scheduler: AsyncIOScheduler = AsyncIOScheduler()

async def on_startup(_):
    print('Bot started')

download_dir = "picts"  # сюда скачиваются картинки форварднутые боту

# проверка на админа
@dp.message_handler(lambda message: message.from_user.id == admin_ID, commands='start')  # стартуем, отправляет сообщение в группу с указанным ID
async def start_message(message: types.Message):
    await bot.send_message(channel_ID, 'Приветствуем вас на канале!')  # отправляем сообщение в канал при старте
    await message.answer(text='Бот запущен', reply_markup=keyboard.kb)  # выводим сообщение в бота и клавиатуру


@dp.message_handler(lambda message: message.from_user.id == admin_ID, commands='pict')  # отправляем фото в группу из каталога
async def post_picture(message: types.Message):
        await post_picture_task()


@dp.message_handler(lambda message: message.from_user.id == admin_ID, commands='start_sched')  # запускаем отправку по расписанию
async def start_scheduler(message: types.Message):
    scheduler.add_job(post_picture_task, 'interval', seconds=post_time())  # выполнение функции постинга по расписанию, задаем время
    scheduler.start()
    await message.answer('Запущена рассылка по расписанию')


@dp.message_handler(lambda message: message.from_user.id == admin_ID, commands='stop_sched')  # останавливаем отправку по расписанию
async def stop_scheduler(message: types.Message):
    scheduler.shutdown(wait=False)
    await message.answer('Остановлена рассылка по расписанию')


@dp.message_handler(lambda message: message.from_user.id == admin_ID, commands='pars')  # стартуем парсинг и проверку на дубли
async def pars_picture(message: types.Message):
    await message.answer('Запускаю парсинг!')
    await pars_pictures_task()  # функция парсинга
    count_files = str(len(os.listdir(path='picts')))  # считаем остаток файлов в каталоге
    await message.answer(f'Закончил парсинг! В каталоге {count_files} файлов.')
    await compare_pictures_task()  # функция проверки картинок на дубли и удаления их
    count_files = str(len(os.listdir(path='picts')))  # считаем остаток файлов в каталоге
    await message.answer(f'Закончил удаление дублей! В каталоге {count_files} файлов.')

@dp.message_handler(lambda message: message.from_user.id == admin_ID, content_types=types.ContentType.PHOTO)  # автоматически скачиваем картинку, которую форварднули
async def handle_photos(message: types.Message):
    if message.photo:
        photo = message.photo[-1]
        file_path = os.path.join(download_dir, f"{photo.file_id}.jpg")
        await bot.download_file_by_id(photo.file_id, file_path)
        await message.answer("Сохранил картинку!")
        await compare_pictures_task()  # функция проверки картинок на дубли и удаления их
        count_files = str(len(os.listdir(path='picts')))  # считаем остаток файлов в каталоге
        await message.answer(f'Закончил удаление дублей! В каталоге {count_files} файлов.')
    else:
        await message.answer("Это не картинка, не могу сохранить!")


@dp.message_handler(lambda message: message.from_user.id == admin_ID)  # сообщения на любую команду не из перечня. парсит картинку из репоста
async def answer(message: types.Message):
    timeout: int = 60
    updates = requests.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1&timeout={timeout}').json()
    pict_id = updates['result'][0]['message']['photo'][-1]['file_id']
    file_path = os.path.join(download_dir, f"{pict_id}.jpg")
    await bot.download_file_by_id(pict_id, file_path)
    print("Сохранил картинку!")
    await compare_pictures_task()  # функция проверки картинок на дубли и удаления их
    count_files = str(len(os.listdir(path='picts')))  # считаем остаток файлов в каталоге
    await message.answer(f'Закончил удаление дублей! В каталоге {count_files} файлов.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
