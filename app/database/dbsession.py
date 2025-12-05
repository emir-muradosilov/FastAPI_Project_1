

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dbconnection import db_connection

engine = create_engine(
    db_connection.DB_URL,
    pool_recycle=1800,
    echo=True,
    )
'''
async_engine = create_async_engine(
    db_connection.async_db_url,
    echo=True,
     future=True,
)
'''

Base = declarative_base()

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

def init_db():
    Base.metadata.create_all(bind=engine)
def init_db():
    Base.metadata.create_all(bind=engine)
