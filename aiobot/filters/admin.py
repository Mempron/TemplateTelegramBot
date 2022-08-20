from aiogram.filters import BaseFilter
from aiogram import types

from ..config import load_config
from ..handlers.admin import admin_router


class IsAdmin(BaseFilter):

    async def __call__(self, message: types.Message) -> bool:
        config = load_config()

        if message.from_user.id == config.bot.admin_id:
            return True
        return False


admin_router.message.filter(IsAdmin())
