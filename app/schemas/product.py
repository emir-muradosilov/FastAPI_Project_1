
from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID, uuid4


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



class ProductCreate(BaseModel):
    pass

class ProductUpdate(BaseModel):
    pass

class ProductDelete(BaseModel):
    pass

class ProductResponse(BaseModel):
    pass



