from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from pydantic import BaseModel
from typing import Optional
from app.database.dbsession import get_db
from app.models.models import Product, Category
from slugify import slugify
from app.schemas.category import CategoryCreate
from app.schemas.product import ProductCreate
from enum import Enum

logger = logging.getLogger(__name__)

router = APIRouter(prefix='', tags=['Router'])

class Item(BaseModel):
    id : int 
    name : str
    is_offer : Optional[bool] = True

# ДОБАВЬТЕ для теста (удалите потом):
@router.get("/")
async def test_root():
    logger.info("Главная страница")
    return {"message": "API работает!", "categories": "/categories"}


@router.post('/create_category')
async def create_category(
    category_data : CategoryCreate,
    db : Session = Depends(get_db)
    ):
    
    slug = slugify(category_data.name)
    uniq_category = db.query(Category).filter(Category.slug == slug).first()

    if uniq_category is not None:
        raise HTTPException(
                status_code=400,
                detail=f"Категория '{category_data.name}' уже существует (ID: {uniq_category.id})"
            ) 
    category = Category(
        name = category_data.name,
        description = category_data.description,
        img = category_data.img,
        slug = slug
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category.id


@router.post('/create_product')
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Создание нового товара
    """
    try:
        # 1. Проверяем, что категория существует
        category = db.query(Category).filter(
            Category.id == product_data.category_id
        ).first()
        
        if not category:
            raise HTTPException(
                status_code=404,
                detail=f"Категория с ID {product_data.category_id} не найдена"
            )
        
        # 2. Генерируем slug
        slug = slugify(product_data.name)
        
        # 3. Проверяем уникальность slug (и товара)
        existing_product = db.query(Product).filter(Product.slug == slug).first()
        if existing_product:
            raise HTTPException(
                status_code=400,
                detail=f"Товар с названием '{product_data.name}' уже существует (ID: {existing_product.id})"
            )
        
        size_value = product_data.size.value if isinstance(product_data.size, Enum) else str(product_data.size)
        color_value = product_data.color.value if isinstance(product_data.color, Enum) else str(product_data.color)
        
        # 4. Создаем товар с правильным category_id
        product = Product(
            name=product_data.name,
            description=product_data.description,
            text=product_data.text,
            img=product_data.img,
            coast=product_data.coast,
            quantity=product_data.quantity,
            size=size_value,           # Enum из схемы
            color=color_value,         # Enum из схемы
            category_id=product_data.category_id,  # Важно: передаем ID, а не объект
            slug=slug
        )
        
        db.add(product)
        db.commit()
        db.refresh(product)
        
        logger.info(f"✅ Товар создан: {product.name} (ID: {product.id})")
        
        return product.id
        
    except HTTPException as e:
        # Пробрасываем HTTP исключения
        raise e
    except Exception as e:
        # Откатываем изменения при любой ошибке
        if 'db' in locals():
            db.rollback()
        logger.error(f"❌ Ошибка при добавлении товара: {str(e)}", exc_info=True)
        
        # Правильное возбуждение исключения
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при добавлении товара: {str(e)}"
        )



# Тестовые функции
@router.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    logger.info("Отправляем данные: item_id: %s, q: %s", item_id, q)
    return {"item_id": item_id, "q": q}

@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Optional[str] = None):
    logger.info("Получены данные: item_name: %s, item_id: %s, текс = %s", item.name, item_id, q)
    return {"item_name": item.name, "item_id": item_id, 'Текст': q }


