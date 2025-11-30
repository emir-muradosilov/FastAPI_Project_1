from dbconnection import db_connection
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    db_connection.DB_URL,
    pool_recycle=5,
    echo=True,
    )

async_engine = create_async_engine(
    db_connection.DB_URL,
    echo=True,
)


Session = sessionmaker(engine)
async_Session = async_sessionmaker(async_engine)


# Создание фабрики сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Зависимость для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

