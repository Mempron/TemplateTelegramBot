from dataclasses import dataclass
import configparser

import logging


logger = logging.getLogger(__name__)


@dataclass
class Bot:
    token: str
    admin_id: int
    use_redis: bool


@dataclass
class Database:
    user: str
    password: str
    name: str
    host: str


@dataclass
class Config:
    bot: Bot
    db: Database


def load_config(path: str = 'config.ini') -> Config:
    config = configparser.ConfigParser()
    config.read(path)

    bot = config['bot']

    return Config(
        bot=Bot(
            token=bot.get('token'),
            admin_id=bot.getint('admin_id'),
            use_redis=bot.getboolean('use_redis')
        ),
        db=Database(**config['db'])
    )
