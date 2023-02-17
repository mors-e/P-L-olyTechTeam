from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from lexicon.lexicon_keyboard import LEXICONKEY


def create_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()

    keyboard.row(*[InlineKeyboardButton(LEXICONKEY[button] if button in LEXICONKEY else button,
                                        callback_data=button) for button in buttons])

    return keyboard


def create_tipic_keyboard(*buttons: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[(LEXICONKEY[button] if button in LEXICONKEY else button) for button in buttons],
                               resize_keyboard=True,
                               one_time_keyboard=True)