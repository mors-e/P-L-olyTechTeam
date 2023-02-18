from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

from keyboard.keyboard import create_inline_kb
from lexicon.lexicon_chat import LEXICONCHATSTAFF
from fsm_state.fsm_state import FSMChatStaff
from database.database import add_message_db


async def chat_start(message: Message):
    await message.answer(text=LEXICONCHATSTAFF['/start_message'], reply_markup=create_inline_kb(2, "chat_hr", "questions"))
    await FSMChatStaff.start.set()


async def chat_hr(callback: CallbackQuery, state):
    await callback.message.answer(text=LEXICONCHATSTAFF['chat_hr'])
    await FSMChatStaff.chat_hr.set()
    await state.finish()


async def questions(callback: CallbackQuery, state):
    async with state.proxy() as data:
        data['quest'] = callback.data
    await callback.message.answer(text=LEXICONCHATSTAFF['questions'])
    await FSMChatStaff.questions.set()


async def await_message(message: Message, state):
    async with state.proxy() as data:
        data['text'] = message.text
        await add_message_db(data, message.from_user.id, message.chat.id)
    await message.answer(text='Вопрос отправлен!')
    await state.finish()


def register_chat_commands_staff(dp: Dispatcher):
    dp.register_message_handler(chat_start, commands=['feedback'])
    dp.register_callback_query_handler(chat_hr, text=['chat_hr'], state=FSMChatStaff.start)
    dp.register_callback_query_handler(questions, text=['questions'], state=FSMChatStaff.start)
    dp.register_message_handler(await_message, lambda x: x.text.isalpha() or not x.text.isalpha(),
                                state=FSMChatStaff.questions)
