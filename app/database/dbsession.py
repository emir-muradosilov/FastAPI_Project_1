from sqlalchemy import create_engine
#from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
from app.models.models import Base

from app.database.dbconnection import DBConnection

from app.models.models import User, Product, Category

db_connection = DBConnection()

engine = create_engine(
    db_connection.DB_URL,
    pool_recycle=1800,
    echo=False,
    )
'''
async_engine = create_async_engine(
    db_connection.async_db_url,
    echo=True,
     future=True,
)
'''


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

