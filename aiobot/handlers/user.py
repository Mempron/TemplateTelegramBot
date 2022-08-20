from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram import types

user_router = Router()


@user_router.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    await message.answer(f'Привет, <b>{message.from_user.full_name}!</b>')
