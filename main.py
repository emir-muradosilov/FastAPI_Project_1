from fastapi import FastAPI
#from . import routers
#from authx import AuthX, AuthXConfig, RequestToken
import logging
import sys
import datetime

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

logger = logging.getLogger(__name__)
#logger.info(f'Logging Started %s', (datetime.datetime.now(),))


# Authx autorization
'''
config = AuthXConfig(
     JWT_ALGORITHM = "HS256",
     JWT_SECRET_KEY = "SECRET_KEY",
     JWT_TOKEN_LOCATION = ["headers"],
     JWT_ACCESS_COOKIE_NAME = 'My cookie'
)

auth = AuthX(config=config)
auth.handle_errors(app)

'''

from app.routes.router import router as urls
# include routes
app.include_router(urls)


# server uvicorn / to start from main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = '127.0.0.1', port = 8081)



    