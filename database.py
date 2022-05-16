from asyncio import current_task
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker
import settings


engine = create_async_engine(
    settings.SQLALCHEMY_ASYNC_URL,
    echo=settings.SQLALCHEMY_ECHO,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
)

async_session_factory = sessionmaker(engine, class_=AsyncSession)

scoped_session = async_scoped_session(async_session_factory, scopefunc=current_task)
