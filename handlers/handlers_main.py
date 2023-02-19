from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from lexicon.lexicon_main import LEXICON
from database.database import add_user, is_staff_user
from keyboard.keyboard import create_keyboard, create_inline_kb


async def start_message(message: Message):
    await message.answer(text=LEXICON['/start_test'], reply_markup=create_keyboard('start_road'))


async def starting_road(callback: CallbackQuery):
    await callback.message.edit_text(text="Давай начнём путь!", reply_markup=create_keyboard('start_test'))


async def starting_road_hr(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON["starting_road_hr"], reply_markup=create_inline_kb(
        1, 'message', 'fsm', 'tsm', 'progress'
    ))


async def starting_road_admin(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['starting_road_admin'], reply_markup=create_inline_kb(
        1, 'delete'
    ))


async def error_starting_road(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['error_starting_road'])


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=['start_test'])
    dp.register_callback_query_handler(starting_road, lambda x: x.data == 'start_road' and
                                       is_staff_user(int(x.from_user.id)) == "staff")
    dp.register_callback_query_handler(starting_road_hr, lambda x: x.data == 'start_road' and
                                       is_staff_user(int(x.from_user.id)) == 'hr')
    dp.register_callback_query_handler(starting_road_admin, lambda x: x.data == 'start_road' and
                                       is_staff_user(int(x.from_user.id)) == 'admin')
    dp.register_callback_query_handler(error_starting_road, lambda x: x.data == 'start_road' and
                                       is_staff_user(int(x.from_user.id)) == "none")