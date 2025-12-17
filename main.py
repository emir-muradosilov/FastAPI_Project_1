from fastapi import FastAPI

import logging
import sys
from app.auth.views import auth, setup_auth
from app.auth.views import router as auth_router
from app.database.dbsession import init_db


# FasrAPI project
app = FastAPI()


# Logging
logging.basicConfig(
#    filename='myapp.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('myapp.log'),  # Логи в файл
        logging.StreamHandler(sys.stdout)  # Логи в консоль
])


setup_auth(app)

# Создаем таблицы при старте
init_db()


from app.routes.router import router as urls
from app.auth.demo_auth.views import router as demo_auth
app.include_router(urls)
app.include_router(auth_router)
app.include_router(demo_auth)



# server uvicorn / to start from main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = '127.0.0.1', port = 8081, reload=True)





