from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from lexicon.lexicon import LEXICON
from database.database import add_user


async def start_message(message: Message):
    await message.answer(text=LEXICON['/start'])
    await add_user(message)
    await message.answer(text="Add")


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=['start'])