
import logging
from fastapi import APIRouter, Depends, Response, HTTPException

from app.models.models import User, Token
from app.database.dbsession import get_db
from app.database.dbasyncsession import async_get_db
from sqlalchemy.orm import Session

import bcrypt
from app.schemas.user import CreateUser, LoginUser
from sqlalchemy import delete, update
#from app.auth.config import config

from fastapi.responses import ORJSONResponse

from authx import AuthXConfig, AuthX

import secrets

from app.schemas.user import *

logger = logging.getLogger(__name__)


config = AuthXConfig(
    JWT_ALGORITHM = 'HS256',
    JWT_SECRET_KEY = 'SECRET_KEY',
    JWT_TOKEN_LOCATION = ['headers'],
    )


def secrets_token_save(
        user_id : int,
        secret_key : str,
        db : Session,
        ) -> bool:
#    try:
#        secret_key = secrets.token_hex()
#    except:
#        raise f'Ошибка генерации Токена'
    try:
        create_secret = Token(user_id = user_id, token = secret_key)
        db.add(create_secret)
        db.commit()
        db.refresh(create_secret)
        return create_secret
    except:
        ValueError("Ошибка сохранения токена")


router = APIRouter(prefix='/autorization', tags = ['Autorization'])

auth = AuthX(config=config)

def setup_auth(app):
    auth.handle_errors(app)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Проверяем пароль
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

@router.post('/login')
async def login(
    response: Response,
    user_data : LoginUser,
    db : Session = Depends(get_db),
    ) -> dict:
    try:
        db_user = db.query(User).filter(User.name == user_data.name).first()
        logger.info('async def login: Пошел запрос в БД на поиск юзера!')
        if db_user is not None:

            # Проверяем пароль с хешированием
            if verify_password(user_data.password, db_user.password):
                token = auth.create_access_token(uid=str(db_user.id))
                response.set_cookie(key="access_token", value=token, httponly=True)

                logger.debug('async def login: Потльзователь найден - Accept!')

                return ORJSONResponse({"access_token": token})
            
            else:
                logger.debug('async def login - HTTPException!')
                raise HTTPException(401, detail={"message": "Invalid credentials"})
        
        else:
            logger.debug('async def login: Потльзователь не найден - db_user is None!')
            raise HTTPException(status_code=401, detail={"message": "Invalid credentials"})
        
    except HTTPException:
            raise  # Пробрасываем HTTPException дальше
    except Exception as e:
        # Логируем ошибку для отладки
        logger.error('async def login - Login error: %s', (e,))
        #print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail={"message": "Internal server error"})


# Hash password
def hash_password(password: str) -> str:
    # Генерируем соль и хешируем пароль
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

@router.post('/registration')
async def registration(
#    response: Response,
    user_data: CreateUser,
#    password: str,
#    profile : Optional[str] = None,
    db : Session = Depends(get_db),
    ):
    
    try:
        existing_user = db.query(User).filter(User.name == user_data.name).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким именем уже существует"
            )
        
        hashed_password = hash_password(user_data.password)
        new_user = User(name = user_data.name, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # получить обновлённый объект из базы
        logger.info('Пользователь %s зарегистрирован', new_user)

        # Создаем JWT токен для автоматического входа
        token = auth.create_access_token(uid=str(new_user.id))

        # Сохранение Токена в БД
        secrets_token_save(user_id=new_user.id, secret_key=token, db=db)

        return {
            "message": "Пользователь успешно зарегистрирован",
            "user_id": new_user.id,
            "username": new_user.name,
            "access_token": token,
            "token_type": "bearer"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        if db:
            db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера при регистрации"
        )


@router.post('/user/{user_id}/deactivate')
async def inactive(user_id, db:Session = Depends(async_get_db)) -> bool:
    try:
        user_update_status = update(User).where(User.id == user_id).values(account_status = False).returning(User.account_status)
        res = await db.execute(user_update_status)
        db.commit()
        return res
    except:
        raise (f'Не получилось обновить статус аккаунта пользователя!')


@router.delete('/user/{user_id}/deactivate', response_model=DeleteUser)
async def inactive():
    user_id : int
    return inactive(user_id)