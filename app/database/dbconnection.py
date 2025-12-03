#from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class DBConnection(BaseSettings):

    db_user : str
    db_pass : str
    db_host : str
    db_port : str
    db_name : str

    @property
    def DB_URL(self):
        return f'postgresql+psycopg2//{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'

    @property
    def async_db_url(self):
        """URL для асинхронного подключения"""
        return f'postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'

config = SettingsConfigDict(
    env_file = '.env',
    env_file_encoding = 'utf-8',
    extra= 'ignore',
)

db_connection = DBConnection()





