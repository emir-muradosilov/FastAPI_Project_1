from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import CreateUser
from sqlalchemy.orm import Session
from app.database.dbasyncsession import async_get_db
from app.models.models import User
from sqlalchemy import delete, insert, select, text
import bcrypt
from fastapi.security import HTTPBearer
import os
from datetime import timedelta
from app.auth.auth_2.auth import UserService, User_Service
from app.schemas.user import LoginUser
import os
from fastapi.security import HTTPBearer
from app.auth.auth_2.config import settings

   

router = APIRouter(prefix='/auto_oop', tags=['Auto_OOP'])

def create_hash_password(password:str):
    hash_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hash_bytes.decode('utf-8')

#def encode_hash_password(password:str):
#        hash_password = bcrypt.hashpw(password.encode(encoding='utf-8'), bcrypt.gensalt().decode('utf-8'))
#        return hash_password

def veryfy_password(user_password, password_from_db):
    hashed_password_bytes = user_password.encode('utf-8')
    password_bytes = password_from_db.encode('utf-8')
    return bcrypt.checkpw(hashed_password_bytes, password_bytes)

@router.post('/')
async def add_user(
    user_data: CreateUser,
    db: Session = Depends(async_get_db)
):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Ошибка в данных')
    
#    user = db.query(User).filter(User.name == user_data.name).first()
    stmt = select(User).where(User.name == user_data.name)
    user = await db.scalar(stmt)
    print(user)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Такой пользователь уже зарегистрирован')
    
    user_add = User(
        name = user_data.name,
        password = create_hash_password(user_data.password),
        login = user_data.login,
        last_name = user_data.last_name,
        middle_name = user_data.middle_name,
        telephone = user_data.telephone,
        email = user_data.email,
        age = user_data.age,
        date_of_birth = user_data.date_of_birth,
        profile = user_data.profile,
        account_status = True
    )
    db.add(user_add)
    await db.commit()
    await db.refresh(user_add)
    return user_add


@router.post('/login', response_model=dict)
async def login(
    data: LoginUser,
    db: Session = Depends(async_get_db)
):
    # 1. Получаем пользователя
    stmt = select(User).where(User.name == data.name)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким именем не найден'
        )

    # 2. Проверяем пароль (с защитой от ошибок bcrypt)
    try:
        password_valid = bcrypt.checkpw(
            data.password.encode('utf-8'),
            user.password.encode('utf-8')
        )
    except ValueError:
        # Если хэш внезапно повреждён
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка проверки пароля'
        )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Некорректный пароль'
        )

    # 3. Генерация токенов
    try:
        access_token_expire = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_token_expire = timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

        access_token = await User_Service.create_token(
            data={'sub': user.name},
            expire_delta=access_token_expire
        )
        refresh_token = await User_Service.create_token(
            data={'sub': user.name},
            expire_delta=refresh_token_expire
        )

    except Exception as e:
        # Любая ошибка JWT / конфигурации
        print('Token error:', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка генерации токена'
        )

    # 4. Успешный ответ
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }











