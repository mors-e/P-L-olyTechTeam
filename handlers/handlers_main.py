from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from lexicon.lexicon_main import LEXICON
from database.database import add_user, is_staff_user
from keyboard.keyboard import create_keyboard


async def start_message(message: Message):
    await message.answer(text=LEXICON['/start'], reply_markup=create_keyboard('/start_road'))
    await add_user(message)


async def starting_road(callback: CallbackQuery):
    await callback.message.edit_text(text="Давай начнём путь!")


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=['start'])
    dp.register_callback_query_handler(starting_road, text="/start_road")