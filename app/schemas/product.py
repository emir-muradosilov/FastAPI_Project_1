
from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID, uuid4
from typing import Optional

class Size(Enum):
    length : str = 'length'
    width : str ='width'
    height : str = 'height'
    weight : str = 'weight'

class Color(Enum):
    red : str = 'Red'
    orange : str = 'Orange'
    yellow : str = 'Yellow'
    green : str = 'Green'
    blue : str = 'Blue'
    purple : str = 'Purple'
    gradient : str = 'Gradient'
    multicolor : str = 'Multicolor'

class ProductBase(BaseModel):
    id : UUID = uuid4(...,) 
    name : str= Field(..., min_length=3, max_length=128, pattern="^[A-Za-z0-9-_]+$")
    description : str = Field(..., min_length=10, max_length=256)
    text : str = Field(min_length=10)
    img : str = Field(...,)
    slug : str = Field(...,)
    coast : float = Field(...,)
    quantity : int = Field(...,)
    size : int = Field(...,)
    color : int = Field(...,)


class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name : Optional[str] = Field(min_length=3, max_length=128, pattern="^[A-Za-z0-9-_]+$")
    description : Optional[str] = Field(min_length=10, max_length=256)
    text : Optional[str] = Field(min_length=10)
    img : Optional[str] = Field()
    slug : Optional[str] = Field()
    coast : Optional[float] = Field()
    quantity : Optional[int] = Field()
    size : Optional[int] = Field()
    color : Optional[int] = Field()

class ProductResponse(ProductBase):
    id : str = Field(...,)



