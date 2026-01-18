import bcrypt
from app.database.dbasyncsession import async_get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.models import User
from datetime import datetime
from jose import jwt, JWTError
from fastapi.security import APIKeyHeader
import os
from authx import AuthXConfig
from fastapi.security import HTTPBearer
from app.auth.auth_2.config import settings



class UserService:


    async def create_hash_password(password:str):
        hash_password = bcrypt.hashpw(password.encode(encoding='utf-8'), bcrypt.gensalt())
        return hash_password

    def verify_hash_password(plain_password: str, hashed_password: str):
        # Проверяем пароль
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )

    async def veryfy_password(self, user_login, user_password, db:Session = Depends(async_get_db)):
        try:
            user = db.query(User).filter(User.name == user_login).first()
            if not user:
                return None
            
            if self.verify_hash_password(user_password, user.password):
                return user
            else:
                return None
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка в пароле: {e}')

    async def autanticate(self, user_login, user_password):
        result = self.veryfy_password(user_login, user_password)
        if result is not None:
            return result
        else:
            return None

    async def create_token(data, expire_delta):
        try:
            payload = data.copy()
            expire = datetime.utcnow() + expire_delta
            payload.update({'exp': expire})
            encode_jwt = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

            return encode_jwt
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка в пароле: {e}')

    async def get_user_by_token(token:str=Depends(APIKeyHeader(name='Authorization')), db:Session = Depends(async_get_db)):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
            username = payload.get('sub')
            user = db.query(User).filter(User.name == username).first()
            return user
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Ошибка авторизации: {e}')



class User_Service:

    async def verify_password(plain_password:str, hashed_password:str):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    async def autenticate_user(username, password, db:Session = Depends(async_get_db)):
        user = await db.query(User).filter(User.name == username).first()
        if not user:
            return None
        return user

    async def create_token(data, expire_delta):
        try:
            payload = data.copy()
            expire = datetime.utcnow() + expire_delta
            payload.update({'exp': expire})
            encode_jwt = jwt.encode(claims=payload, key = settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

            return encode_jwt
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка в пароле: {e}')

    async def get_user_by_token(token:str=Depends(APIKeyHeader(name='Authorization')), db:Session = Depends(async_get_db)):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
            username = payload.get('sub')
            user = db.query(User).filter(User.name == username).first()
            return user
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Ошибка авторизации: {e}')






