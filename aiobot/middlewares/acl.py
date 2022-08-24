from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Update, User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.user import User


class AccessControlListMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            update: Update,
            data: Dict[str, Any]
    ) -> Any:

        user_data: TelegramUser = data.get('event_from_user')
        if not user_data:
            return await handler(update, data)

        session: AsyncSession = data.get('session')
        query = select(User).where(User.telegram_id == user_data.id)
        user = await session.execute(query)

        try:
            user = user.scalar()
        except AttributeError:
            return await handler(update, data)

        if user.ban:
            return

        data['user'] = user

        return await handler(update, data)
