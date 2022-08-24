from aiogram import Dispatcher
from aiogram.dispatcher.middlewares.user_context import UserContextMiddleware

from ..utils.sessionmaker import create_sessionmaker
from ..config import Config
from ..middlewares.database import DatabaseMiddleware
from ..middlewares.config import ConfigMiddleware
from ..middlewares.acl import AccessControlListMiddleware
from ..handlers.user import user_router
from ..handlers.admin import admin_router


async def include_all_middlewares(dp: Dispatcher, config: Config) -> None:
    dp.update.outer_middleware(UserContextMiddleware())
    dp.update.outer_middleware(ConfigMiddleware(config))
    dp.update.outer_middleware(DatabaseMiddleware(await create_sessionmaker(config)))
    dp.update.outer_middleware(AccessControlListMiddleware())


def include_all_routers(dp: Dispatcher) -> None:
    dp.include_router(admin_router)
    dp.include_router(user_router)


async def include_all_routers_middlewares(dp: Dispatcher, config: Config) -> None:
    await include_all_middlewares(dp, config)
    include_all_routers(dp)
