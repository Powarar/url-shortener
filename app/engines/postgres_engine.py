from sqlalchemy.ext.asyncio import AsyncResult, async_sessionmaker, AsyncSession, create_async_engine
import logging
from typing import Any
from app.settings import settings
from app.models.base import BaseDB
from sqlalchemy.exc import IntegrityError, InterfaceError, OperationalError, ProgrammingError

log = logging.getLogger(__name__)

class PostgresEngine:
    def __init__(self):
        self.engine = create_async_engine(
        url=f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}',
        )
        self.session = async_sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False)


    async def create_tables(self) -> None:
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(BaseDB.metadata.create_all)
        except (OperationalError, ProgrammingError, InterfaceError) as err:
            log.error(msg=f'PostgresEngine: method create_tables crashed: {err.orig}', exc_info=False)

    async def drop_tables(self) -> None:
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(BaseDB.metadata.drop_all)
        except (OperationalError, ProgrammingError, InterfaceError) as err:
            log.error(msg=f'PostgresEngine: method drop_tables crashed: {err.orig}', exc_info=False)

    async def execute(self, stmt: BaseDB, no_return: bool = False, return_many: bool = False) -> Any:
        try:
            async with self.async_session() as session:
                cursor: AsyncResult = await session.execute(stmt)  # noqa
                await session.commit()
                if no_return:
                    return None
                if return_many:
                    return cursor.scalars().all()
                return cursor.scalar_one_or_none()
        except IntegrityError as err:
            log.error(msg=f'PostgresEngine: method execute crashed: {err.__class__.__name__}', exc_info=True)
        except (OperationalError, ProgrammingError, InterfaceError) as err:
            log.error(msg=f'PostgresEngine: method execute crashed: {err.__class__.__name__}', exc_info=False)
        finally:
            await session.close()

db_engine = PostgresEngine()