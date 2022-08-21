from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class DatabaseMiddleware(BaseMiddleware):

    def __init__(self, async_sessionmaker) -> None:
        super().__init__()
        self.async_sessionmaker = async_sessionmaker

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        async with self.async_sessionmaker() as session:
            data['session'] = session
            return await handler(event, data)
