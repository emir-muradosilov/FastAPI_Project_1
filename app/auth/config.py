
from authx import AuthXConfig

import os

config = AuthXConfig(
JWT_ALGORITHM = 'HS256',
JWT_SECRET_KEY = 'SECRET_KEY',
JWT_TOKEN_LOCATION = ['headers',],
    )


