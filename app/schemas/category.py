from pydantic import BaseModel, Field
from typing import Optional

class CategoryCreate(BaseModel):
    name : str = Field(..., min_length=4, max_length= 124)
    description : str = Field(..., min_length=4, max_length= 256)
#    slug : str = Field(..., min_length=4, max_length= 124)
    img : str = Field(..., min_length=4, max_length= 124)

class CategoryUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    img : Optional[str] = None

class CategoryResponse(BaseModel):
    id : int
    name : Optional[str] = None
    description : Optional[str] = None
    slug : Optional[str] = None
    img : Optional[str] = None
