from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def create_main_kb():
    main_kb = ReplyKeyboardBuilder()
    main_kb.row(types.KeyboardButton(text='Проверить номер'))
    main_kb.row(types.KeyboardButton(text='Проверить базу'))

    return main_kb


def create_phone_kb():
    phone_kb = InlineKeyboardBuilder()
    phone_kb.add(types.InlineKeyboardButton(text='Отмена действия',
                                            callback_data='cancel'))
    return phone_kb