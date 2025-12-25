
from authx import AuthXConfig
from fastapi.security import HTTPBearer
import os

config = AuthXConfig(
JWT_ALGORITHM = 'HS256',
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY'),
JWT_TOKEN_LOCATION = ['headers',],
security = HTTPBearer()
    )


