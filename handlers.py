from time import time

from aiogram import types, Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from utils.selenium_func import selenium_work
from utils.validate import validate_phone_number, edit_number
from utils.states import PhoneNumber
from utils.keyboards import create_main_kb, create_phone_kb
from utils.delete_messages import try_delete_prev_message, add_message_for_delete
from utils.excel import get_excel
from db.queries import add_record, check_record


main_router = Router()


@main_router.message(Command('start'))
async def main_page(message: types.Message,
                    state: FSMContext,
                    bot: Bot,
                    text='Главное меню'):
    await try_delete_prev_message(bot, state)

    main_kb = create_main_kb()
    msg = await message.answer(text=text,
                               reply_markup=main_kb.as_markup(resize_keyboard=True,
                                                              one_time_keyboard=True))
    await state.update_data(prev_msg=list())
    data = await state.get_data()

    add_message_for_delete(data, msg)

    try:
        await message.delete()
    except TelegramBadRequest:
        pass
    

@main_router.message(F.text == 'Проверить номер')
async def check_phone_number(message: types.Message,
                             state: FSMContext,
                             bot: Bot,
                             text='Введи номер'):
    await try_delete_prev_message(bot, state)

    phone_kb = create_phone_kb()

    await state.set_state(PhoneNumber.number)
    msg = await message.answer(f'{text}\nНомер должен содержать только цифры, длина номера - 11 символов\nДопускается "+" в начале номера',
                         reply_markup=phone_kb.as_markup())
    
    await state.update_data(prev_msg=list())
    data = await state.get_data()

    add_message_for_delete(data, msg)

    await message.delete()


@main_router.message(F.text == 'Проверить базу')
async def check_db(message: types,
                   state: FSMContext,
                   session: Session,
                   engine: Engine,
                   bot: Bot):
    await try_delete_prev_message(bot, state)

    text = await get_excel(message, engine)

    await main_page(message,
                    state,
                    bot,
                    text=text)


@main_router.callback_query(F.data == 'cancel')
async def cancel_action(callback: types.CallbackQuery,
                        state: FSMContext,
                        bot: Bot):
    await callback.answer()
    await main_page(callback.message,
                state,
                bot)

#####################################
@main_router.message(F.text == 'тест')
async def test(message: types.Message,
               session: Session):
    number = '89992233041'
    response = 'qwerty'

    try:
        add_record(session, number, response)
    except SQLAlchemyError as ex:
        print(ex)
        await message.answer('Не получилось добавить в базу')
    else:
        await message.answer(f'Номер: {number}\nИмя: {response}')
#######################################


@main_router.message(PhoneNumber.number)
async def get_receiver_name(message: types.Message,
                            state: FSMContext,
                            session: Session,
                            bot: Bot):
    await try_delete_prev_message(bot, state)

    start_time = time()
    phone_number = message.text

    if validate_phone_number(phone_number):
        phone_number = edit_number(phone_number)

        if check_record(session, phone_number):
            text = 'Номер телефона уже есть в базе'
            await main_page(message,
                            state,
                            bot,
                            text=text)
        else:
            msg = await message.answer('Номер обрабатывается...\nПримерное время обработки: 15-20c')

            response =  await selenium_work(phone_number)

            if response.startswith('Ошибка'):
                text = (f'{response}\nПопробуйте повторить позже.')

            else:
                try:
                    add_record(session,
                            phone_number,
                            response)
                except SQLAlchemyError as ex:
                    print(ex)
                    text = 'Не получилось добавить в базу'
                else:
                    text = f'Номер: {phone_number}\n Имя: {response}'
            
            await state.update_data(prev_msg=list())
            data = await state.get_data()

            add_message_for_delete(data, msg)

            await main_page(message,
                            state,
                            bot,
                            text=text)

    else:
        text = 'Некорректный ввод, проверьте номер\nПоддерживаются только российские номера'
        await check_phone_number(message,
                                state,
                                bot,
                                text=text)

    end = time()
    print(f'выполнено за {end-start_time}c')
