

from authx import AuthXConfig, AuthX, RequestToken
#from main import app, auth
from fastapi import HTTPException, Depends, Response
from sqlalchemy.orm import Session
from app.database import dbsession
from models.models import User, Category, Product
from passlib.context import CryptContext
import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/categories",  # опционально: префикс для всех маршрутов
    tags=["Categories"]    # опционально: теги для документации
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


auth = None

def set_auth(auth_instance):
    """Функция для установки auth из main.py"""
    global auth
    auth = auth_instance


class CategoryService:
    
    @staticmethod
    def create_user(): #registration
        pass

    @staticmethod
    def delete_user():
        pass

    @staticmethod
    def autirization(): # authorization
        pass

    @staticmethod
    def edit_user():
        pass

@router.get('/')
async def index():
    context = {'hello' : 'Hello world!'}
    return


@router.get('/login')
async def login(username: str, password: str, db : Session = Depends(dbsession.get_db), response = Response):
    try:
        db_user = db.query(User).filter(User.name == username).one_or_none()
        if db_user is not None:
            db_password = db_user.password

            '''
            if username == db_user.name and password == db_password:
                token = auth.create_access_token(uid=username)
                return {"access_token": token}
            '''
            # Проверяем пароль с хешированием
            if pwd_context.verify(password, db_user.password):
                token = auth.create_access_token(uid=db_user.id)
                response.set_cookie()

                logger.debug('async def login - Accept!')
                return {"access_token": token}
            else:

                logger.debug('async def login - HTTPException!')
                raise HTTPException(401, detail={"message": "Invalid credentials"})
        
        else:
            logger.debug('async def login - db_user is None!')
            return HTTPException(401, detail={"message": "Invalid credentials"})
        
    except HTTPException:
            raise  # Пробрасываем HTTPException дальше
    except Exception as e:
        # Логируем ошибку для отладки
        logger.error('async def login - Login error: %s', (e,))
        #print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail={"message": "Internal server error"})



@router.get("/protected", dependencies=[Depends(auth.get_token_from_request)])
def get_protected(token: RequestToken = Depends()):
    try:
        auth.verify_token(token=token)
        return {"message": "Hello world !"}
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e
     

