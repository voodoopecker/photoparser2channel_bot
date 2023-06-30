from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

btn1 = KeyboardButton('/pict')  # разместить картинку
btn2 = KeyboardButton('/start_sched')  # старт рассылки по расписанию
btn3 = KeyboardButton('/stop_sched')  # стоп рассылки по расписанию
btn4 = KeyboardButton('/pars')  # начать парсинг картинок
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.row(btn1, btn4).add(btn2, btn3)