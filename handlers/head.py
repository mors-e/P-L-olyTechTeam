import asyncio

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher import FSMContext

from database.database import page_prez, update, get_photo, select_all_pages, is_correct_quest, result_test
from keyboard.keyboard import create_pagination_keyboard, create_keyboard
from lexicon.lexicon_quest import LEXICON
from fsm_state.fsm_state import FSMQuest


async def process_beginning_command(message: Message):
    id_number: int = page_prez(message.from_user.id)
    await message.answer_photo(photo='AgACAgIAAxkBAAICnWPxCJ6ZslBnEMpWZMgrngdrG2ILAAJLxDEbCQKJS28GzbFAuOQjAQADAgADeQADLgQ',
                               reply_markup=create_pagination_keyboard(
        "backward", f"{id_number}", "forward"
    ))


async def process_forward(callback: CallbackQuery):
    try:
        id_number: int = page_prez(callback.from_user.id)
        if id_number < select_all_pages():
            await callback.message.delete()
            await update(callback.from_user.id, id_number + 1)
            id_number: int = page_prez(callback.from_user.id)
            await callback.message.answer_photo(photo=get_photo(id_number),
                                                 reply_markup=create_pagination_keyboard(
                                                   "backward", f"{id_number}", "forward"
                                               ))
        else:
            await callback.answer()
            await callback.message.answer(text="Хотите пройти опрос?", reply_markup=create_keyboard(
                'Пройти опрос'
            ))
    except MessageNotModified:
        await callback.answer()


async def start_quest(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['one'], reply_markup=create_keyboard(
                                          'crylo', 'ros', 'mos', 'sir'))

    await FSMQuest.start.set()


async def two_quest(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['quest_1'] = callback.data

    await callback.message.edit_text(text=LEXICON['two'], reply_markup=create_keyboard(
        '2.1', '2.2', '2.3', '2.4'))

    await FSMQuest.quest1.set()


async def three_quest(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['quest_2'] = callback.data

    await callback.message.edit_text(text=LEXICON['three'], reply_markup=create_keyboard(
        '3.1', '3.2', '3.3', '3.4'))

    await FSMQuest.quest2.set()


async def four_quest(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['quest_3'] = callback.data

    await callback.message.edit_text(text=LEXICON['four'], reply_markup=create_keyboard(
        '4.1', '4.2', '4.3', '4.4'))

    await FSMQuest.quest3.set()


async def five_quest(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['quest_4'] = callback.data

    await callback.message.edit_text(text=LEXICON['five'], reply_markup=create_keyboard(
        '5.1', '5.2', '5.3', '5.4'))

    await FSMQuest.quest4.set()


async def ending_quest(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['quest_5'] = callback.data

    async with state.proxy() as data:
        task = asyncio.create_task(is_correct_quest(data.as_dict()))

        await task

    await callback.message.edit_text(text=f"Вы завершили тестирование с резальтатом:"
                                          f" {result_test(int(callback.from_user.id))}")

    await state.finish()


async def process_backward(callback: CallbackQuery):
    try:
        id_number: int = page_prez(callback.from_user.id)
        if id_number > 1:
            await callback.message.delete()
            await update(callback.from_user.id, id_number - 1)
            id_number: int = page_prez(callback.from_user.id)
            print(get_photo(id_number))
            await callback.message.answer_photo(photo=get_photo(id_number),
                                                reply_markup=create_pagination_keyboard(
                                                  "backward", f"{id_number}", "forward"
                                              ))
        else:
            await callback.answer()
    except MessageNotModified:
        await callback.answer()


def register_head_handlers(dp: Dispatcher):
    dp.register_message_handler(process_beginning_command, commands=['begin'])
    dp.register_callback_query_handler(process_forward, text=['forward'])
    dp.register_callback_query_handler(process_backward, text=['backward'])
    dp.register_callback_query_handler(start_quest, text=['Пройти опрос'])
    dp.register_callback_query_handler(two_quest, text=['crylo', 'ros', 'mos', 'sir'], state=FSMQuest.start)
    dp.register_callback_query_handler(three_quest, text=['2.1', '2.2', '2.3', '2.4'], state=FSMQuest.quest1)
    dp.register_callback_query_handler(four_quest, text=['3.1', '3.2', '3.3', '3.4'], state=FSMQuest.quest2)
    dp.register_callback_query_handler(five_quest, text=['4.1', '4.2', '4.3', '4.4'], state=FSMQuest.quest3)
    dp.register_callback_query_handler(ending_quest, text=['5.1', '5.2', '5.3', '5.4'], state=FSMQuest.quest4)



