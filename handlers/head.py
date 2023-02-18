import asyncio

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageNotModified

from database.database import page_prez, update, get_photo, select_all_pages
from keyboard.keyboard import create_pagination_keyboard


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
    except MessageNotModified:
        await callback.answer()


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