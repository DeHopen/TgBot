#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.filters import Text
from aiogram.types import CallbackQuery

from config import API_TOKEN, admin, admin1
from src.keyboard import *
import function as func
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from src.states import *

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
connection = sqlite3.connect('data.db')
q = connection.cursor()

@dp.message_handler(commands=['start'])
async def start(message):
    func.join(message.chat.id)
    await message.answer(f"Привет {message.from_user.first_name}!\n\n"
                         "Благодарим за проявленный интерес к нашей услуге.\n\n"
                         "Мы 🚗 доставляем готовые кальяны на дом, ресторан, банкет..... по Москве и МО.\n"
                         "📦Доставка в пределах МКАД БЕСПЛАТНАЯ*, за пределами МКАД, уточняется у менеджера.\n\n"
                         "Кальян забираем на следующий день в удобное для Вас время.\n"
                         "Кальян можно не мыть, просто слейте воду и положите в сумку.\n\n"
                         "⚠️Отвечая здесь, Вы даете согласие на обработку персональных данных:\n"
                         "your-hookah.ru/personal-data.html\n\n"
                         "Выберите один из вариантов ниже:", reply_markup=main_menu())

# если нажали кнопку "Зказать" то надо спрашивать сколько кальянов нужно и сохранять эти данные в базу данных
@dp.message_handler(text="Заказать")
async def order(message):
    await message.answer("Сколько кальянов нужно?", reply_markup=remove_kb())
    await UserState.wait_number_hoockah.set()
# после того как пользователь ввел количество кальянов, надо узнать какой крепости он хочет табак, по дестибальной шкале и потом сохранить это в базу данных
@dp.message_handler(state=UserState.wait_number_hoockah)
async def order(message, state: FSMContext):
    await state.update_data(number_hoockah=message.text)
    await message.answer("Какой крепости табак?", reply_markup=remove_kb())
    await UserState.wait_tobacco_strength.set()
# после того как пользователь ввел крепость табака, надо узнать какой вкус табака он хочет и потом сохранить это в базу данных
@dp.message_handler(state=UserState.wait_tobacco_strength)
async def order(message, state: FSMContext):
    await state.update_data(tobacco_strength=message.text)
    await message.answer("Какой вкус табака?", reply_markup=remove_kb())
    await UserState.wait_tobacco_flavor.set()
# после того как пользователь ввел вкус табака, надо узнать какие 3 чаши в комплект он хочет и потом сохранить это в базу данных
@dp.message_handler(state=UserState.wait_tobacco_flavor)
async def order(message, state: FSMContext):
    await state.update_data(tobacco_flavor=message.text)
    await message.answer("Какую чашу вы хотите в комплект?", reply_markup=chashi())
    await UserState.wait_cup.set()
# после того как пользователь ввел какие 3 чаши в комплект он хочет, надо узнать полный адрес клиента и потом сохранить это в базу данных
@dp.message_handler(state=UserState.wait_cup)
async def order(message, state: FSMContext):
    await state.update_data(cup=message.text)
    await message.answer("Введите полный адрес доставки:\n\n"
                         "КВАРТИРА\n"
                         "ЭТАЖ\n"
                         "ПОДЬЕЗД\n"
                         "ДОМОФОН\n", reply_markup=cancel())
    await UserState.wait_info_about_order.set()
# после того как пользователь ввел полный адрес доставки, надо узнать номер телефона клиента и потом сохранить это в базу данных
@dp.message_handler(state=UserState.wait_info_about_order)
async def order(message, state: FSMContext):
    await state.update_data(info_about_order=message.text)
    await message.answer("Введите номер телефона:", reply_markup=cancel())
    await UserState.wait_phone_number.set()
#после того как пользователь ввел номер телефона, надо спросить его об удобном времени доставки и сделать это inline кнопками и потом сохранить это в базу данных
@dp.message_handler(state=UserState.wait_phone_number)
async def order(message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer("Когда Вам удобно доставить кальян?", reply_markup=time())
    await UserState.wait_time.set()

# после того как пользователь ввел удобное время доставки, надо отправить ему все что он ввел и дать возможность его отредактировать или отправить и потом сохранить это в базу данных и отправить админу
@dp.message_handler(state=UserState.wait_phone_number)
@dp.callback_query(Text(text=['yes', 'no']))
async def order(message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    data = await state.get_data()
    await message.answer(f"Ваш заказ:\n\n"
                         f"Количество кальянов: {data.get('number_hoockah')}\n"
                         f"Крепость табака: {data.get('tobacco_strength')}\n"
                         f"Вкус табака: {data.get('tobacco_flavor')}\n"
                         f"Чаша: {data.get('cup')}\n"
                         f"Адрес доставки: {data.get('info_about_order')}\n"
                         f"Номер телефона: {data.get('phone_number')}\n"
                         f"Время доставки: {data.get('time')}\n\n"
                         f"Все верно?", reply_markup=yes_or_no())
    await UserState.wait_correct.set()
# если пользователь нажал кнопку "Да" то надо отправить ему сообщение что заказ принят и отправить админу сообщение с заказом

@dp.message_handler(state=UserState.wait_correct)
async def order(call, state: FSMContext):
    if 'Да' in call.data:
        await call.message.answer("Ваш заказ принят, ожидайте звонка оператора.", reply_markup=main_menu(), parse_mode='HTML')
        await state.finish()
    else:
        await call.message.answer("Введите заново.", reply_markup=main_menu(), parse_mode='HTML')
        await state.finish()
# если пользователь нажал кнопку "Нет" то надо отправить ему сообщение что заказ отменен и отправить админу сообщение с отменой заказа
@dp.message_handler(state=UserState.wait_correct)
async def order(call, state: FSMContext):
    if 'Нет' in call.data:
        await call.message.answer("Ваш заказ отменен.", parse_mode='HTML', reply_markup=main_menu())
        await state.finish()
    else:
        await call.message.answer("Введите заново.", reply_markup=main_menu(), parse_mode='HTML')
        await state.finish()
# если пользователь нажимает на кнопку "Отмена" то надо отправить ему сообщение что заказ отменен
@dp.message_handler(content_types= ['text'], text = "Отменить")
async def order(message, state: FSMContext):
        await message.answer("Ваш заказ отменен.", reply_markup=main_menu())
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






