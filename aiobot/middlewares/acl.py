from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Update, User
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User


class AccessControlListMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            update: Update,
            data: Dict[str, Any]
    ) -> Any:

        user_data: User = data.get('event_from_user')
        if not user_data:
            return

        session: AsyncSession = data.get('session')

        user = await session.get(User, {'id': user_data.id})

        if not user:
            user = User(id=user_data.id)
            session.add(user)
            await session.commit()

        data['user'] = user

        return await handler(update, data)
