from fastapi import FastAPI
#from . import routers
#from authx import AuthX, AuthXConfig, RequestToken
import logging
import sys
import datetime
from app.auth.config import auth, setup_auth
from app.auth.config import router as auth_router
from app.database.dbsession import init_db

# FasrAPI project
app = FastAPI()


# Logging
# FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(
#    filename='myapp.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('myapp.log'),  # Логи в файл
        logging.StreamHandler(sys.stdout)  # Логи в консоль
])

#logger = logging.getLogger(__name__)
#logger.info(f'Logging Started %s', (datetime.datetime.now(),))
setup_auth(app)

# Создаем таблицы при старте
init_db()


from app.routes.router import router as urls
app.include_router(urls)
app.include_router(auth_router)

# server uvicorn / to start from main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = '127.0.0.1', port = 8081)



    