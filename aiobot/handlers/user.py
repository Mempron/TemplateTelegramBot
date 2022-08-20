from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User

user_router = Router()


@user_router.message(CommandStart())
async def start_handler(message: types.Message, session: AsyncSession) -> None:

    session.add(User(message.from_user.id))

    await message.answer(f'Привет, <b>{message.from_user.full_name}!</b>\nЯ создал запись о тебе в моей таблице.')
