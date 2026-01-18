from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from app.database.dbsession import get_db
from app.database.dbasyncsession import async_get_db
from app.models.models import Product, Category
from slugify import slugify
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from enum import Enum
from sqlalchemy import delete, func, select, text
from app.services.services import _slug_creator 

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/Product', tags=['Product'])



@router.post('/create_product', response_model=ProductResponse)
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
        slug_count = await _slug_creator(product_data.name, Product)
        slug = str(slugify(product_data.name))+'-'+str(slug_count)
        
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
        
        return product
        
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


@router.patch('/update_product_by_id/', response_model= ProductResponse)
async def update_product(id : int, product_date : ProductUpdate, db:Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == id).first()
        
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Продукт для редактрирования не найден!')

        update_product_date = product_date.model_dump(exclude_unset=True)
        
        if not update_product_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Нет данных для обноления!')
        
        for key,value in update_product_date.items():
            setattr(product, key, value)
        
        db.add(product)
        db.commit()
        db.refresh(product)

        return product
    
    except Exception as e:
        
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Ошибка обновления товара {e}')

@router.delete('/delete_product_by_id', response_model=dict)
async def delete_product(id:int, db:Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка при поиске товара на удаление {e}')
        
        delete_product = delete(Product).where(Product.id == id)
        db.execute(delete_product)
        db.commit()
        return {'message': 'Товар был удален!'}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка при удалении товара {e}')


@router.get('/get_product_by_id', response_model=ProductResponse)
async def get_product(id:int, db:Session=Depends(get_db)):
    try:
        product = db.query(Product).filter(Category.id == id).first()
        return product
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Ошибка при отображении товара {e}')
    
@router.get('/get_product_list')
async def get_product(db:Session=Depends(get_db)):
    try:
        res = db.execute(select(Product))
        ss = db.execute(text('Select * From table_name join table_name_second On table_name.column = table_name_second.column Where table_name_second.column=5'))
        print(res)
        product_list = res.scalars().all()
        return {'product':product_list}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Ошибка при отображении товара {e}')

@router.post('/update_test', response_model=dict)
async def update_test(id: int, data:ProductUpdate, db:Session=Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise 'Нет данного товара'
        
        product_data = data.model_dump(exclude_unset=True)
        for key,value in product_data.items():
            setattr(product,key,value)
        db.add(product)
        db.commit()
        db.refresh(product)
        return {'Данные успешно обновлены':product}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка {e}')

@router.get('/delete_test', response_model=dict)
async def delete_test(id:int, db:Session=Depends(async_get_db)):
    try:
        product = db.query(Product).filter(Product.id==id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка. Такого товара нет!')
        delete_product = delete(product).where(Product.id == id)
        db.execute(delete_product)
        db.commit()
        return {'message':'Товар успешно удален!'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка {e}')
    
@router.post('/add_product_test', response_model=ProductResponse)
async def product_add_test(product_data:ProductCreate, db :Session = Depends(async_get_db)):
    try:
        if not product_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка во входных данных')
        
#        slug_name = select(Product).where(Product.slug == product_data.name)
        stmt = select(Product).where(Product.slug == product_data.name)
        result = await db.execute(stmt)
        existing_product = result.scalar_one_or_none()
        if existing_product:
            max_id = select(func.max(Product.id))
            result  = await db.execute(max_id)
            existing_product = result.scalar_one_or_none()
            slug = str(product_data.name)+'-'+str(existing_product)
        size_value = product_data.size.value if isinstance(product_data.size, Enum) else str(product_data.size)
        color_value = product_data.color.value if isinstance(product_data.color, Enum) else str(product_data.color)


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
        await db.commit()
        await db.refresh(product)
        return product
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка при сохранении: {e}')
