from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

kb_inline_builder_confirm = InlineKeyboardBuilder()
kb_inline_builder_confirm.add(
    InlineKeyboardButton(text='Да', callback_data='yes'),
    InlineKeyboardButton(text='Нет', callback_data='no'),
)
