
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.database.dbconnection import DBAsyncConnect
from app.models.models import Base

dbconnection = DBAsyncConnect()

async_engine = create_async_engine(
    dbconnection.ASYNC_DB_URL,
    pool_pre_ping=True,
    future = True,
    echo = False,
    pool_recycle=3600,
    )


# Создание фабрики сессий
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
#    bind=async_engin,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Зависимость для получения сессии
async def async_get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # Автоматический коммит при успехе
        except Exception:
            await session.rollback()  # Откат при ошибке
            raise
        finally:
            await session.close()


async def init_db():
    async with async_engine.begin() as conn:
    # Создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)



