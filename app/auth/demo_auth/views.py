
from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from app.database.dbsession import get_db
from sqlalchemy.orm import Session
from app.schemas.user import LoginUser
from app.models.models import User, Token
import secrets
import bcrypt

router = APIRouter(prefix='/demo-auth', tags=['Demo Auth'])

security = HTTPBasic()

@router.get('/basic-auth/')
async def demo_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        'message':'Hi',
        'username': credentials.username,
        'password': credentials.password,
        }

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Проверяем пароль
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )


async def get_auth_user_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        db: Session = Depends(get_db),
) -> User | str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password',
        headers={'WWW-Authentificate':'Basic'},
    )
    try:

        user = db.query(User).filter(User.name == credentials.username).first()
        print('Из БД ', user.name)
        print('Из запроса ', credentials.username)

    except:
        raise unauthed_exc
    if user is not None:
        if credentials.username not in user.name:
            return unauthed_exc
        '''
        if not secrets.compare_digest(
            credentials.password.encode('utf-8'),
            user.password.encode('utf-8')
            ):
            raise unauthed_exc
        '''
        if verify_password(credentials.password,user.password):

            return credentials.username
    else:
        raise unauthed_exc

@router.get('/basic-auth-username/')
async def demo_basic_auth_username(
    auth_username : str = Depends(get_auth_user_username)
    ):
    return {
        'message':f'Hi {auth_username},',
        'username': auth_username
        }

def get_user_by_static_token(db:Session = Depends(get_db), token: str = Header(alias='static-auth-token')):
    try:
        user = db.query(User).join(Token, User.id == Token.user_id).filter(Token.token == token).first()
        if user is not None:
            return user.name
        else:
            raise ('Ошибка при получение пользователя')
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token invalid')


@router.get('/some-http-header-auth/')
async def demo_some_http_header_auth(
    auth_username : str = Depends(get_user_by_static_token)
    ):
    return {
        'message':f'Hi {auth_username},',
        'username': auth_username
        }

@router.get('/login-cookie/')
async def demo_auth_login_cookie(
    auth_username : str = Depends(get_user_by_static_token)
    ):
    return {
        'message':f'Hi {auth_username},',
        'username': auth_username
        }
