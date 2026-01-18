from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from pydantic import BaseModel
from typing import Optional
from app.database.dbsession import get_db
from app.models.models import Category
from slugify import slugify
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from sqlalchemy import delete, func, select, update
from app.services.services import _slug_creator 

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/Category', tags=['Category'])

class Item(BaseModel):
    id : int 
    name : str
    is_offer : Optional[bool] = True


@router.post('/create_category', response_model=CategoryResponse)
async def create_category(
    category_data : CategoryCreate,
    db : Session = Depends(get_db)
    ):

    slug_count = await _slug_creator(category_data.name, Category, db)
    slug = str(slugify(category_data.name))+'-'+str(slug_count)

    uniq_category = db.query(Category).filter(Category.name == category_data.name).first()

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
    return category

@router.patch('/update_category_by_id', response_model= CategoryResponse)
async def update_category(id:int, category_data: CategoryUpdate, db:Session=Depends(get_db)):
    try:
        category = db.query(Category).filter(Category.id == id).first()

        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Категория не найдена')
        
        category_update_data = category_data.model_dump(exclude_unset=True)
        if not category_update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Нет данных для обноления')
        
        for key,value in category_update_data.items():
            setattr(category, key,value)

        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка при редактировании данных {e}')

@router.delete('/delete_category_by_id', response_model=dict)
async def delete_category(id: int, db:Session=Depends(get_db)):
    try:
        category = db.query(Category).filter(Category.id == id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка категория не найдена')
        category_delete = delete(Category).where(Category.id == id)
        db.execute(category_delete)
        db.commit()

        return {'message': 'Данная категория успешно удалена'}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка при удалении категории {e}')


@router.get('/get_category_by_id', response_model=dict)
async def get_category(id:int, db:Session = Depends(get_db)):
    try:
        category = db.query(Category).filter(Category.id == id).first()
        return category
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Ошибка при запросе Категории {e}')

@router.get('/get_category_list')
async def get_category_list(db:Session = Depends(get_db)):
    try:
        res = db.execute(select(Category))
        category_list = res.scalars().all()
        return {'category':category_list}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка при выводе всех Категорий {e}')

@router.get('/get_category_list_by_params')
async def get_category_list(param_name:str, param_data:int, db:Session = Depends(get_db)):
    try:
        category_list = db.query(Category).filter(Category.param_name == param_data).all()
        return {'category':category_list}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка при выводе всех Категорий {e}')

