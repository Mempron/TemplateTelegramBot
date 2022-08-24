import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from redis import Redis

from aiobot.config import load_config, Config
from aiobot.utils.regist import include_all_routers_middlewares


logging.basicConfig(
    format='%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s',
    level=10
)
logger = logging.getLogger(__name__)


async def main() -> None:
    config: Config = load_config()

    bot = Bot(config.bot.token, parse_mode='HTML')
    storage = RedisStorage(Redis) if config.bot.use_redis else MemoryStorage()
    dp = Dispatcher(storage=storage)

    await include_all_routers_middlewares(dp, config)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()

        try:
            await bot.session.close()
        except AttributeError:
            logger.error('Can not close the bot\'s session.')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.critical('The bot stopped!')
