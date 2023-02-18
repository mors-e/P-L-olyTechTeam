from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageNotModified
from database.database import is_staff_user, add_ban_list


async def check_staff(message: Message):
    if is_staff_user(int(message.from_user.id)) == 'none':
        await message.answer(text="Добро пожаловать! В ближайшее время вашу"
                                  " заявку рассмотрит руководитель отдела, ожидайте")
        await add_ban_list(message.from_user.id)
    elif is_staff_user(int(message.from_user.id)) == "ban":
        await message.answer(text="Вашу заявку руководитель не одобрил, вы не являетесь сотрудником!")
    else:
        await message.answer(text='С возвращением!')


def register_admin(dp: Dispatcher):
    dp.register_message_handler(check_staff, commands=['start'])