from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext

from lexicon.lexicon_fsm import LEXICONFSM
from keyboard.keyboard import create_keyboard, create_inline_kb
from fsm_state.fsm_state import FSMFillForm
from servises.servises import is_valid, is_valid_fio, is_valid_date


async def process_cancel(message: Message, state: FSMContext):
    await message.answer(text='Вы отменили прохождение теста')
    await state.reset_state()


async def process_start_fsm(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICONFSM['email'], reply_markup=None)

    await FSMFillForm.email.set()


async def process_send_email(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text

    await message.answer(text=LEXICONFSM['FIO_user'])

    await FSMFillForm.FIO_user.set()


async def warning_send_email(message: Message):
    await message.answer(text=LEXICONFSM['email_warning'])


async def process_send_fio(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio'] = message.text

    await message.answer(text=LEXICONFSM['division'])

    await FSMFillForm.division.set()


async def warning_send_fio(message: Message):
    await message.answer(text=LEXICONFSM['FIO_user_warning'])


async def process_send_division(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['division'] = message.text

    await message.answer(text=LEXICONFSM['FIO_leader'])

    await FSMFillForm.FIO_leader.set()


async def warning_send_division(message: Message):
    await message.answer(text=LEXICONFSM['warning_send_division'])


async def process_send_fio_leader(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio_leader'] = message.text

    await message.answer(text=LEXICONFSM['date_start_working'])

    await FSMFillForm.date_start_working.set()


async def warning_send_fio_leader(message: Message):
    await message.answer(text=LEXICONFSM['FIO_leader_warning'])


async def process_send_data(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['data'] = message.text

    await message.answer(text=LEXICONFSM['rate_expectations'], reply_markup=create_inline_kb(
        5, *[str(a) for a in range(1, 11)]
    ))

    await FSMFillForm.rate_expectations.set()


async def warning_send_data(message: Message):
    await message.answer(text=LEXICONFSM['warning_send_data'])


async def process_rate_expectations(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['rate'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['full_expectations'])

    await FSMFillForm.full_expectations.set()


async def warning_rate_expectations(message: Message):
    await message.answer(text=LEXICONFSM['warning_rate_expectations'], reply_markup=create_inline_kb(
        5, *[str(a) for a in range(1, 11)]
    ))


async def process_full_expectations(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_expectations'] = message.text

    await message.answer(text=LEXICONFSM['college_revue'], reply_markup=create_inline_kb(
        3, 'yes_ex', 'no_ex', 'im_ex', 'more'
    ))

    await FSMFillForm.college_revue.set()


async def warning_full_expectations(message: Message):
    await message.answer(text=LEXICONFSM['warning_full_expectations'])


def register_fsm_handlers(dp: Dispatcher):
    dp.register_message_handler(process_cancel, commands=['cancel'], state='*')
    dp.register_callback_query_handler(process_start_fsm, lambda x: x.data == "start_test")
    dp.register_message_handler(process_send_email, lambda x: is_valid(x.text), state=FSMFillForm.email)
    dp.register_message_handler(warning_send_email, content_types='any', state=FSMFillForm.email)
    dp.register_message_handler(process_send_fio, lambda x: is_valid_fio(x.text), state=FSMFillForm.FIO_user)
    dp.register_message_handler(warning_send_fio, content_types='any', state=FSMFillForm.FIO_user)
    dp.register_message_handler(process_send_division, lambda x: x.text.isalpha(), state=FSMFillForm.division)
    dp.register_message_handler(warning_send_division, content_types='any', state=FSMFillForm.division)
    dp.register_message_handler(process_send_fio_leader, lambda x: is_valid_fio(x.text), state=FSMFillForm.FIO_leader)
    dp.register_message_handler(warning_send_fio_leader, content_types='any', state=FSMFillForm.FIO_leader)
    dp.register_message_handler(process_send_data, lambda x: is_valid_date(x.text), state=FSMFillForm.date_start_working)
    dp.register_message_handler(warning_send_data, content_types='any', state=FSMFillForm.date_start_working)
    dp.register_callback_query_handler(process_rate_expectations, text=[str(a) for a in range(1, 11)],
                                       state=FSMFillForm.rate_expectations)
    dp.register_message_handler(warning_rate_expectations, content_types='any', state=FSMFillForm.rate_expectations)
    dp.register_message_handler(process_full_expectations, lambda x: x.text.isalpha() or not x.text.isalpha(),
                                state=FSMFillForm.full_expectations)
    dp.register_message_handler(warning_full_expectations, content_types='any', state=FSMFillForm.full_expectations)
