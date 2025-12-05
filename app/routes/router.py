from fastapi import APIRouter
import logging
from pydantic import BaseModel
from typing import Optional


logger = logging.getLogger(__name__)

router = APIRouter()

class Item(BaseModel):
    id : int 
    name : str
    is_offer : Optional[bool] = True

# ДОБАВЬТЕ для теста (удалите потом):
@router.get("/")
async def test_root():
    logger.info("Главная страница")
    return {"message": "API работает!", "categories": "/categories"}


# Тестовые функции
@router.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    logger.info("Отправляем данные: item_id: %s, q: %s", item_id, q)
    return {"item_id": item_id, "q": q}

@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Optional[str] = None):
    logger.info("Получены данные: item_name: %s, item_id: %s, текс = %s", item.name, item_id, q)
    return {"item_name": item.name, "item_id": item_id, 'Текст': q }


