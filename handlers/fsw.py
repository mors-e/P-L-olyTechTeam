import asyncio

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext

from lexicon.lexicon_fsm import LEXICONFSM
from keyboard.keyboard import create_keyboard, create_inline_kb
from fsm_state.fsm_state import FSMFillForm
from servises.servises import is_valid, is_valid_fio, is_valid_date
#from database.database import add_week_one


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


async def process_college_revue(callback: CallbackQuery, state: FSMContext):
    if callback.data != 'more':
        async with state.proxy() as data:
            data['college_revue'] = callback.data

        await callback.message.edit_text(text=LEXICONFSM['college_intimate'], reply_markup=create_inline_kb(
            2, 'yes_col', 'no_col', 'more_col'
        ))

        await FSMFillForm.college_intimate.set()
    else:
        await callback.message.edit_text(text=LEXICONFSM['process_full_expectations_more'])
        await FSMFillForm.college_revue_more.set()


async def process_full_expectations_more(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['college_revue'] = message.text

    await message.answer(text=LEXICONFSM['college_intimate'], reply_markup=create_inline_kb(
        2, 'yes_col', 'no_col', 'more_col'
    ))

    await FSMFillForm.college_intimate.set()


async def warning_full_expectations_more(message: Message):
    await message.answer(text=LEXICONFSM['warning_full_expectations'])


async def warning_college_revue(message: Message):
    await message.answer(text=LEXICONFSM['inline_error'], reply_markup=create_inline_kb(
        3, 'yes_ex', 'no_ex', 'im_ex', 'more'
    ))


async def process_college_intimate(callback: CallbackQuery, state: FSMContext):
    if callback.data != "more_col":
        async with state.proxy() as data:
            data['college_intimate'] = callback.data

        await callback.message.edit_text(text=LEXICONFSM['college_other'], reply_markup=create_inline_kb(
            3, 'yes_col_i', 'few', 'our', 'more_other'
        ))

        await FSMFillForm.college_other.set()
    else:
        await callback.message.edit_text(text=LEXICONFSM['text_more'])
        await FSMFillForm.college_intimate_more.set()


async def process_college_revue_more(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['college_intimate'] = message.text

    await message.answer(text=LEXICONFSM['college_other'], reply_markup=create_inline_kb(
            1, 'yes_col_i', 'few', 'our', 'more_other'
        ))
    await FSMFillForm.college_other.set()


async def process_college_other(callback: CallbackQuery, state: FSMContext):
    if callback != "more_other":
        async with state.proxy() as data:
            data['college_other'] = callback.data

        await callback.message.edit_text(text=LEXICONFSM['your_duties'], reply_markup=create_inline_kb(
            1, 'd_yes', 'd_no', 'd_more'
        ))
        await FSMFillForm.your_duties.set()
    else:
        await callback.message.edit_text(text=LEXICONFSM['text_more'])
        await FSMFillForm.college_other_more.set()


async def more_college_other(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['college_other'] = message.data

    await message.answer(text=LEXICONFSM['your_duties'], reply_markup=create_inline_kb(
        1, 'd_yes', 'd_no', 'd_more'
    ))

    await FSMFillForm.your_duties.set()


async def warning_college_other(message: Message):
    await message.answer(text=LEXICONFSM['inline_error'], reply_markup=create_inline_kb(
            1, 'yes_col_i', 'few', 'our', 'more_other'
        ))


async def warning_college_intimate(message: Message):
    await message.answer(text=LEXICONFSM['inline_error'], reply_markup=create_inline_kb(
        2, 'yes_col', 'no_col', 'more_col'
    ))


async def process_your_duties(callback: CallbackQuery, state: FSMContext):
    if callback.data != 'more_other':
        async with state.proxy() as data:
            data['duties'] = callback.data

        await callback.message.edit_text(text=LEXICONFSM['leader_task'], reply_markup=create_inline_kb(
            2, 'l_task', 'l_no_task', 'l_more'
        ))
        await FSMFillForm.leader_task.set()
    else:
        await callback.message.edit_text(text=LEXICONFSM['text_more'])
        await FSMFillForm.college_other_more.set()


async def more_college_intimate(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['duties'] = message.text

    await message.answer(text=LEXICONFSM['leader_task'], reply_markup=create_inline_kb(
        2, 'l_task', 'l_no_task', 'l_more'
    ))
    await FSMFillForm.leader_task.set()


async def warning_your_duties(message: Message):
    await message.answer(text=LEXICONFSM['inline_error'], reply_markup=create_inline_kb(
        1, 'd_yes', 'd_no', 'd_more'
    ))


async def process_leader_task(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['leader_task'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['leader_task_solve'], reply_markup=create_inline_kb(
        1, 'yes_lead', 'sometimes', 'no_lead', 'lead_more'
    ))

    await FSMFillForm.leader_task_solve.set()


async def process_leader_task_solve(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['leader_task_solve'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['tasks_hard'], reply_markup=create_inline_kb(
        1, 'Да', 'Нет', 'Другое'
    ))
    await FSMFillForm.tasks_hard.set()


async def process_tasks_hard(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['tasks_hard'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['address_colleagues_questions'], reply_markup=create_inline_kb(
        1, 'yes_adcq', 'som_adcq', 'no_adsq', 'more_adcq'
    ))
    await FSMFillForm.address_colleagues_questions.set()


async def process_address_colleagues_questions(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['address_colleagues_questions'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['address_leader_questions'], reply_markup=create_inline_kb(
        1, 'yes_alq', 'som_alq', 'no_alq', 'im_alq', 'more_alq'
    ))
    await FSMFillForm.address_leader_questions.set()


async def process_address_leader_questions(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['address_leader_questions'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['helping_questions'], reply_markup=create_inline_kb(
        1, 'collegs', 'rukovod', 'imsearch', 'more_hq'
    ))
    await FSMFillForm.helping_questions.set()


async def process_helping_questions(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['helping_questions'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['leader_feedback'], reply_markup=create_inline_kb(
        1, 'yes_lf', 'no_lf', 'more_lf'
    ))
    await FSMFillForm.leader_feedback.set()


async def process_leader_feedback(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['leader_feedback'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['tutor'])

    await FSMFillForm.tutor.set()


async def process_tutor(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['process_tutor'] = message.text

    await message.answer(text=LEXICONFSM['launch'])

    await FSMFillForm.launch.set()


async def process_launch(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['launch'] = message.text

    await message.answer(text=LEXICONFSM['launch_people'], reply_markup=create_inline_kb(
        1, 'with_col', 'alone', 'more_lp'
    ))

    await FSMFillForm.launch_people.set()


async def process_launch_people(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['launch_people'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['contact_colleagues'], reply_markup=create_inline_kb(
        1, 'yes_cc', 'no_cc', 'more_cc'
    ))

    await FSMFillForm.contact_colleagues.set()


async def process_contact_colleagues(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['contact_colleagues'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['sick'], reply_markup=create_inline_kb(
        2, 'Да', 'Нет'
    ))

    await FSMFillForm.sick.set()


async def process_sick(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['sick'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['income'], reply_markup=create_inline_kb(
        2, 'Да', 'Не совсем'
    ))

    await FSMFillForm.income.set()


async def process_income(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['income'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['holiday'], reply_markup=create_inline_kb(
        2, 'Да', 'Не знаю'
    ))

    await FSMFillForm.holiday.set()


async def process_holiday(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['holiday'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['structure_company'], reply_markup=create_inline_kb(
        3, 'Да', 'Нет', 'Немного представляю', 'Другое'
    ))

    await FSMFillForm.structure_company.set()


async def process_structure_company(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['structure_company'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['operations_divisions'], reply_markup=create_inline_kb(
        1, 'only_ad', 'some_od', 'under_od', 'more'
    ))

    await FSMFillForm.operations_divisions.set()


async def process_operations_divisions(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['operations_divisions'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['covering_divisions'], reply_markup=create_inline_kb(
        1, 'iknow', 'somek', 'inear', 'iwould', 'more'
    ))

    await FSMFillForm.covering_divisions.set()


async def process_covering_divisions(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['covering_divisions'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['subordinate_institutions'], reply_markup=create_inline_kb(
        1, 'Да', 'Не совсем', 'Знаю только названия', 'А что это такое?', 'Не изучал', 'more'
    ))

    await FSMFillForm.subordinate_institutions.set()


async def process_subordinate_institutions(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['subordinate_institutions'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['working_comfort'], reply_markup=create_inline_kb(
        5, *[str(a) for a in range(1, 11)]
    ))

    await FSMFillForm.working_comfort.set()


async def process_working_comfort(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['working_comfort'] = callback.data

    await callback.message.edit_text(text=LEXICONFSM['comfort'])

    await FSMFillForm.comfort.set()


async def process_comfort(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['comfort'] = message.text

    await message.answer(text=LEXICONFSM['other'])

    await FSMFillForm.other.set()


async def process_other(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['comfort'] = message.text

    await message.answer(text="Ура, опрос завершён!")

    async with state.proxy() as data:
        task = asyncio.create_task(add_week_one(message, data))

        await task

    await state.finish()


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
    dp.register_callback_query_handler(process_college_revue, text=['yes_ex', 'no_ex', 'im_ex', 'more'],
                                       state=FSMFillForm.college_revue)
    dp.register_message_handler(process_full_expectations_more, lambda x: x.text.isalpha() or not x.text.isalpha(),
                                state=FSMFillForm.college_revue_more)
    dp.register_message_handler(warning_full_expectations_more, content_types='any',
                                state=FSMFillForm.college_revue_more)
    dp.register_message_handler(warning_college_revue, content_types='any', state=FSMFillForm.college_revue)
    dp.register_callback_query_handler(process_college_intimate, text=['yes_col', 'no_col', 'more_col'],
                                       state=FSMFillForm.college_intimate)
    dp.register_message_handler(process_college_revue_more, lambda x: x.text.isalpha() or not x.text.isalpha(),
                                state=FSMFillForm.college_intimate_more)
    dp.register_message_handler(warning_college_intimate, content_types='any',
                                state=FSMFillForm.college_intimate)
    dp.register_callback_query_handler(process_college_other, text=['yes_col_i', 'few', 'our', 'more_other'],
                                       state=FSMFillForm.college_other)
    dp.register_message_handler(more_college_other, lambda x: x.text.isalpha() or not x.text.isalpha(),
                                state=FSMFillForm.college_other_more)
    dp.register_message_handler(warning_college_other, content_types='any', state=FSMFillForm.college_other)
    dp.register_callback_query_handler(process_your_duties, text=['d_yes', 'd_no', 'd_more'],
                                       state=FSMFillForm.your_duties)
    dp.register_message_handler(more_college_intimate, lambda x: x.text.isalpha() or not x.text.isalpha(),
                                state=FSMFillForm.your_duties_more)
    dp.register_message_handler(warning_your_duties, content_types='any', state=FSMFillForm.your_duties)
    dp.register_callback_query_handler(process_leader_task, text=['l_task', 'l_no_task', 'l_more'],
                                       state=FSMFillForm.leader_task)
    dp.register_callback_query_handler(process_leader_task_solve,
                                       text=['yes_lead', 'sometimes', 'no_lead', 'lead_more'],
                                       state=FSMFillForm.leader_task_solve)
    dp.register_callback_query_handler(process_tasks_hard, text=['Да', 'Нет', 'Другое'], state=FSMFillForm.tasks_hard)
    dp.register_callback_query_handler(process_address_colleagues_questions, text=['yes_adcq', 'som_adcq', 'no_adsq', 'more_adcq'],
                                       state=FSMFillForm.address_colleagues_questions)
    dp.register_callback_query_handler(process_address_leader_questions, text=['yes_alq', 'som_alq', 'no_alq', 'im_alq', 'more_alq'],
                                       state=FSMFillForm.address_leader_questions)
    dp.register_callback_query_handler(process_helping_questions, text=['collegs', 'rukovod', 'imsearch', 'more_hq'],
                                       state=FSMFillForm.helping_questions)
    dp.register_callback_query_handler(process_leader_feedback, text=['yes_lf', 'no_lf', 'more_lf'],
                                       state=FSMFillForm.leader_feedback)
    dp.register_message_handler(process_tutor, lambda x: is_valid_fio(x.text),
                                state=FSMFillForm.tutor)
    dp.register_message_handler(process_launch, lambda x: x.text.isalpha() or not x.text.isalpha(),
                                state=FSMFillForm.launch)
    dp.register_callback_query_handler(process_launch_people, text=['with_col', 'alone', 'more_lp'],
                                       state=FSMFillForm.launch_people)
    dp.register_callback_query_handler(process_contact_colleagues, text=['yes_cc', 'no_cc', 'more_cc'],
                                       state=FSMFillForm.contact_colleagues)
    dp.register_callback_query_handler(process_sick, text=['Да', 'Нет'],
                                       state=FSMFillForm.sick)
    dp.register_callback_query_handler(process_income, text=['Да', 'Не совсем'],
                                       state=FSMFillForm.income)
    dp.register_callback_query_handler(process_holiday, text=['Да', 'Не знаю'],
                                       state=FSMFillForm.holiday)
    dp.register_callback_query_handler(process_structure_company, text=['Да', 'Нет', 'Немного представляю', 'Другое'],
                                       state=FSMFillForm.structure_company)
    dp.register_callback_query_handler(process_operations_divisions, text=['only_ad', 'some_od', 'under_od', 'more'],
                                       state=FSMFillForm.operations_divisions)
    dp.register_callback_query_handler(process_covering_divisions, text=['iknow', 'somek', 'inear', 'iwould', 'more'],
                                       state=FSMFillForm.covering_divisions)
    dp.register_callback_query_handler(process_subordinate_institutions,
                                       text=['Да', 'Не совсем', 'Знаю только названия',
                                             'А что это такое?', 'Не изучал', 'more'],
                                       state=FSMFillForm.subordinate_institutions)
    dp.register_callback_query_handler(process_working_comfort, text=[str(a) for a in range(1, 11)],
                                       state=FSMFillForm.working_comfort)
    dp.register_message_handler(process_comfort, lambda x: x.text.isalpha() or not x.text.isalpha(),
                                state=FSMFillForm.comfort)
    dp.register_message_handler(process_other, lambda x: x.text.isalpha() or not x.text.isalpha(),
                                state=FSMFillForm.other)











