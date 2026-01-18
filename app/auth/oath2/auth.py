from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from fastapi import APIRouter

router = APIRouter(prefix='/oath2', tags=['oAth2'])


#app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}