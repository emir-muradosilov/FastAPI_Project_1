from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name : str = Field(..., min_length=4, max_length= 124)
    description : str = Field(..., min_length=10, max_length= 256)
    slug : str = Field(..., min_length=4, max_length= 124)
    img : str = Field(..., min_length=4, max_length= 124)

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id : str = Field(...,)
