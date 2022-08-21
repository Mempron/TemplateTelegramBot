import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.dispatcher.middlewares.user_context import UserContextMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from redis import Redis

from aiobot.config import load_config
from aiobot.models.database import Base
from aiobot.middlewares.database import DatabaseMiddleware
from aiobot.middlewares.acl import AccessControlListMiddleware
from aiobot.handlers.user import user_router
from aiobot.handlers.admin import admin_router

logging.basicConfig(
    format='%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s',
    level=10
)
logger = logging.getLogger(__name__)


def setup_all_middlewares(dp: Dispatcher, async_sessionmaker: sessionmaker) -> None:
    dp.update.outer_middleware(UserContextMiddleware())
    dp.update.outer_middleware(DatabaseMiddleware(async_sessionmaker))
    dp.update.outer_middleware(AccessControlListMiddleware())


def include_all_routers(dp: Dispatcher) -> None:
    dp.include_router(admin_router)
    dp.include_router(user_router)


async def main() -> None:
    config = load_config()

    engine = create_async_engine(
        f'postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.name}',
        echo=False
    )
    async with engine.begin() as connection:
        # await connection.run_sync(Base.metadata.drop_all)  # Drop tables!
        await connection.run_sync(Base.metadata.create_all)

    async_sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    bot = Bot(config.bot.token, parse_mode='HTML')
    storage = RedisStorage(Redis) if config.bot.use_redis else MemoryStorage()
    dp = Dispatcher(storage=storage)

    setup_all_middlewares(dp, async_sessionmaker)
    include_all_routers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()

        try:
            await bot.session.close()
        except AttributeError:
            logger.error('Can not close the bot\'s session.')

        await engine.dispose()


if __name__ == '__main__':

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.critical('The bot stopped!')
