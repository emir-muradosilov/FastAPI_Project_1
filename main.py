from fastapi import FastAPI
#from . import routers
from authx import AuthX, AuthXConfig, RequestToken
import logging


app = FastAPI() 



# Logging
log = logging.getLogger(__name__)

def main():
    FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
    logging.basicConfig(filename='myapp.log', level=logging.INFO, format=FORMAT)
    log.info('Started')

    log.info('Finished')


# Authx autorization
config = AuthXConfig(
     JWT_ALGORITHM = "HS256",
     JWT_SECRET_KEY = "SECRET_KEY",
     JWT_TOKEN_LOCATION = ["headers"],
     JWT_ACCESS_COOKIE_NAME = 'My cookie'
)

auth = AuthX(config=config)
auth.handle_errors(app)

from app.services.category import router as category_router
# include routes
app.include_router(category_router)


# server uvicorn / to start from main
if __name__ == "__maine__":
    import uvicorn
    uvicorn.run(app, host = '127.0.0.1', port = 8081)



    