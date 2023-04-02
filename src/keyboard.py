from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

def remove_kb():
    kb = ReplyKeyboardRemove()
    return kb

def main_menu():
    main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu.add(
        types.KeyboardButton('Заказать'),
        types.KeyboardButton('Мои заказы'),
        types.KeyboardButton('Контакты')
    )
    return main_menu

def chashi():
    chashi = types.ReplyKeyboardMarkup(resize_keyboard=True)
    chashi.add(
        types.KeyboardButton('Классика'),
        types.KeyboardButton('Грейпфрут'),
        types.KeyboardButton('Гранат'),
        types.KeyboardButton('Ананас'),
    )
    chashi.add('Вернуться')
    return chashi
def time():
    time = types.InlineKeyboardMarkup(row_width=3)
    time.add(
        types.InlineKeyboardButton(text='с 10 до 13', callback_data='first'),
        types.InlineKeyboardButton(text='с 13 до 16', callback_data='second'),
        types.InlineKeyboardButton(text='с 16 до 19', callback_data='third'),
        types.InlineKeyboardButton(text='с 19 до 22', callback_data='fourth'),
    )
    time.add(types.InlineKeyboardButton(text='Мне удобно в определенное время', callback_data='certain'))
    return time
#сделать inline кнопки да и нет
def yes_or_no():
    yes_or_no = types.InlineKeyboardMarkup(row_width=2)
    yes_or_no.add(
        types.InlineKeyboardButton(text='ДА', callback_data='yes'),
        types.InlineKeyboardButton(text='НЕТ', callback_data='no')
    )
    return yes_or_no
def cancel():
    cancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel.add(
        types.KeyboardButton('Отменить')
    )
    return cancel