from main import app
import logging
from fastapi import APIRouter, Depends, Response, HTTPException

from app.models.models import User
from app.database.dbsession import get_db
from sqlalchemy.orm import Session

import auth
from passlib.context import CryptContext
from authx import AuthXConfig, AuthX, RequestToken

logger = logging.getLogger(__name__)

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get('/login')
async def login(username: str, password: str, db : Session = Depends(get_db), response: Response = Depends()):

    try:
        db_user = db.query(User).filter(User.name == username).one_or_none()
        if db_user is not None:
            db_password = db_user.password

            # Проверяем пароль с хешированием
            if pwd_context.verify(password, db_user.password):
                token = auth.create_access_token(uid=db_user.id)
                response.set_cookie(key="access_token", value=token, httponly=True)

                logger.debug('async def login - Accept!')
                return {"access_token": token}
            else:

                logger.debug('async def login - HTTPException!')
                raise HTTPException(401, detail={"message": "Invalid credentials"})
        
        else:
            logger.debug('async def login - db_user is None!')
            raise HTTPException(status_code=401, detail={"message": "Invalid credentials"})
        
    except HTTPException:
            raise  # Пробрасываем HTTPException дальше
    except Exception as e:
        # Логируем ошибку для отладки
        logger.error('async def login - Login error: %s', (e,))
        #print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail={"message": "Internal server error"})