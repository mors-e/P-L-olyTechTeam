from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher

from keyboard.keyboard import create_inline_kb
from lexicon.lexicon_chat import LEXICONCHATHR
from fsm_state.fsm_state import FSMChatHR
from database.database import (is_message, add_message_db_hr, change_status_questions,
                               is_staff_user)


async def chat_start(message: Message):
    await message.answer(text=LEXICONCHATHR['/start_request'], reply_markup=create_inline_kb(1, "request"))
    await FSMChatHR.start.set()


async def chat_start_error(message: Message):
    await message.answer(text="Вы не является hr для этой команды!")


async def request(callback: CallbackQuery, state):
    async with state.proxy() as data:
        data['req'] = callback.data
    if is_message() is not None:
        await callback.message.answer(text=f"Вопрос от 'tg://user?id={is_message()[3]}':\n{is_message()[1]}\n{LEXICONCHATHR['await_request']}")
        await FSMChatHR.request.set()
    else:
        await callback.message.answer(text='No new message')
        await state.finish()


async def await_request(message: Message, state):
    async with state.proxy() as data:
        data['text'] = message.text
        data['id_massage'] = f'{is_message()[0]}'
        data['id_user'] = f'{message.from_user.id}'
        data['chat_id'] = f'{is_message()[4]}'
        await change_status_questions(data['id_massage'])
        await add_message_db_hr(data)
        await message.send_copy(data['chat_id'], message_thread_id=message.message_thread_id,
                                reply_to_message_id=data['id_massage'])
    await message.answer(text='Ответ отправлен!')
    await state.finish()


def register_chat_commands_hr(dp: Dispatcher):
    dp.register_message_handler(chat_start_error, lambda x: x.text == '/start_request'
                                                            and is_staff_user(int(x.from_user.id)) == 'staff')
    dp.register_message_handler(chat_start, lambda x: x.text == '/start_request'
                                                      and is_staff_user(int(x.from_user.id)) == 'hr')
    dp.register_callback_query_handler(request, lambda x: x.data == 'request'
                                                         and is_staff_user(int(x.from_user.id)) == 'hr',
                                       state=FSMChatHR.start)
    dp.register_message_handler(await_request, lambda x: (x.text.isalpha() or not x.text.isalpha())
                                                         and is_staff_user(int(x.from_user.id)) == 'hr',
                                state=FSMChatHR.request)
