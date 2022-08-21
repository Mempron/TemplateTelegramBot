from aiogram.filters import BaseFilter
from aiogram import types

from ..config import Config


class IsAdmin(BaseFilter):

    async def __call__(self, message: types.Message, *args, **kwargs) -> bool:
        data = kwargs
        config: Config = data.get('config')

        if message.from_user.id == config.bot.admin_id:
            return True
        return False
