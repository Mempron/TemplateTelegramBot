from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..models.database import Base
from ..config import Config


async def create_sessionmaker(config: Config) -> sessionmaker:
    engine = create_async_engine(
        f'postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.name}',
        echo=False
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)  # Drop tables!
        await connection.run_sync(Base.metadata.create_all)

    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
