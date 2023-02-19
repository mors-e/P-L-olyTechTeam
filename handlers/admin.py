import asyncio

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext

from database.database import (is_staff_user, add_ban_list, add_user, watch_ban_list,
                               update_ban_list)
from keyboard.keyboard import create_keyboard
from fsm_state.fsm_state import FSMRuk


async def check_staff(message: Message):
    if is_staff_user(int(message.from_user.id)) == 'none':
        await message.answer(text="Добро пожаловать! В ближайшее время вашу"
                                  " заявку рассмотрит руководитель отдела, ожидайте")
        await add_user(message, post='none')
        await add_ban_list(int(message.from_user.id))
    elif is_staff_user(int(message.from_user.id)) == "ban":
        await message.answer(text="Вашу заявку руководитель не одобрил, вы не являетесь сотрудником!")
    else:
        await message.answer(text='С возвращением!')


async def is_staff_or_ban(message: Message):
    await message.answer(text="Список запросов на сотрудника", reply_markup=create_keyboard('Посмотреть'))

    await FSMRuk.start.set()


async def ban_list_watching(callback: CallbackQuery, state: FSMContext):
    id_user: int = watch_ban_list()
    if id_user is not None:
        async with state.proxy() as data:
            data['person'] = id_user

        await callback.message.edit_text(text=f"Является ли tg://user?id={id_user} новым сотрудником компании?",
                                         reply_markup=create_keyboard('Да', 'Нет'))

        await FSMRuk.load.set()
    else:
        await state.finish()
        await callback.message.edit_text(text="Список пуст, возвращайтесь возже!")


async def apply(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['apply'] = callback.data

    async with state.proxy() as data:
        task = asyncio.create_task(update_ban_list(data.as_dict()))

        await task

    await state.finish()

    await callback.message.edit_text(text=f"Продолжить просмотр списка?", reply_markup=create_keyboard('Посмотреть'))


async def reppit(callback: CallbackQuery):
    await callback.message.edit_text(text="Список запросов на сотрудника", reply_markup=create_keyboard('Посмотреть'))

    await FSMRuk.start.set()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(check_staff, commands=['start'])
    dp.register_message_handler(is_staff_or_ban, lambda x: x.text == '/ban_list' and
                                is_staff_user(int(x.from_user.id)) == 'admin')
    dp.register_callback_query_handler(ban_list_watching, text=['Посмотреть'], state=FSMRuk.start)
    dp.register_callback_query_handler(apply, text=['Да', 'Нет'], state=FSMRuk.load)
    dp.register_callback_query_handler(reppit, text=['Посмотреть'])
