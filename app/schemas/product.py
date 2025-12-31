
from pydantic import BaseModel, Field, validator
from enum import Enum
from uuid import UUID, uuid4
from typing import Optional
from enum import Enum as PyEnum

class Size(str, PyEnum):
    length : str = 'length'
    width : str ='width'
    height : str = 'height'
    weight : str = 'weight'

class Color(str, PyEnum):
    red : str = 'Red'
    orange : str = 'Orange'
    yellow : str = 'Yellow'
    green : str = 'Green'
    blue : str = 'Blue'
    purple : str = 'Purple'
    gradient : str = 'Gradient'
    multicolor : str = 'Multicolor'

class ProductCreate(BaseModel):
#    id : int = Field(...,)
    name : str= Field(..., min_length=3, max_length=128)
    description : str = Field(..., max_length=256)
    text : str = Field(max_length=256)
    img : str = Field(...,)
#    slug : str = Field(...,)
    coast : float = Field(...,)
    quantity : int = Field(...,)
    size : Size
    color : Color
    category_id: int

    @validator('size', pre=True)
    def validate_size(cls, v):
        """Валидация размера - должен быть одним из Size"""
        if isinstance(v, str):
            v = v.lower()  # Приводим к нижнему регистру
            if v not in ['length', 'width', 'height', 'weight']:
                raise ValueError(
                    f'Недопустимый размер: {v}. '
                    f'Допустимые значения: length, width, height, weight'
                )
        return v

    @validator('color', pre=True)
    def validate_color(cls, v):
        """Валидация цвета - должен быть одним из Color"""
        if isinstance(v, str):
            # Приводим к правильному формату
            if v.lower() == 'red':
                v = 'Red'
            elif v.lower() == 'orange':
                v = 'Orange'
            elif v.lower() == 'yellow':
                v = 'Yellow'
            elif v.lower() == 'green':
                v = 'Green'
            elif v.lower() == 'blue':
                v = 'Blue'
            elif v.lower() == 'purple':
                v = 'Purple'
            elif v.lower() == 'gradient':
                v = 'Gradient'
            elif v.lower() == 'multicolor':
                v = 'Multicolor'
            else:
                raise ValueError(
                    f'Недопустимый цвет: {v}. '
                    f'Допустимые значения: Red, Orange, Yellow, Green, Blue, Purple, Gradient, Multicolor'
                )
        return v


class ProductUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    text : Optional[str] = None
    img : Optional[str] = None
#    slug : Optional[str] = Field()
    coast : Optional[float] = None
    quantity : Optional[int] = None
    size : Optional[Size] = None
    color : Optional[Color] = None

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id : int
    name : Optional[str] = None
    description : Optional[str] = None
    text : Optional[str] = None
    img : Optional[str] = None
#    slug : Optional[str] = Field()
    coast : Optional[float] = None
    quantity : Optional[int] = None
    size : Optional[Size] = None
    color : Optional[Color] = None



