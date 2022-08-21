from typing import Dict

from aiogram.filters import BaseFilter
from aiogram import types

from ..config import Config


class IsAdmin(BaseFilter):

    async def __call__(self, message: types.Message, data: Dict) -> bool:

        config: Config = data.get('config')
        print(config)

        if message.from_user.id == config.bot.admin_id:
            return True
        return False
