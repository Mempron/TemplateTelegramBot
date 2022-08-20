from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram import types

admin_router = Router()


@admin_router.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    await message.answer(f'Приветствую, хозяин!')
