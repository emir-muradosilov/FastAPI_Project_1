from pydantic import BaseModel, field_validator, Field, ConfigDict, EmailStr
from enum import Enum
from uuid import UUID, uuid4
from datetime import date
from typing import Optional



class Profile(str, Enum):
    Seller : str = 'Seller'
    Buyer : str = 'Buyer'

'''
class UserBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Иван",
                "last_name": "Иванов",
                "middle_name": "Иванович",
                "telephone": "+79991234567",
                "email": "ivan@example.com",
                "age": 25,
                "date_of_birth": "1998-05-15",
                "profile": "Buyer",
                "account_status": True
            }
        }
    )


@field_validator('date_of_birth')
@classmethod
def chek_valid_date(clc, date_of_birth: date):
    today = date.today()
    eighteen_years_ago = date(today.year - 18, today.month, today.day)
    if date_of_birth > eighteen_years_ago:
        raise ValueError("Employees must be at least 18 years old.")
    return date_of_birth
'''

class CreateUser(BaseModel):
    name : str = Field(...,)
    login:str = Field(...,)
    password : str = Field(...,)
    last_name : str = Field() # Фамилия
    middle_name : str = Field() # Отчество
    telephone : str = Field()
    email : str = Field()
#    email : str = Field(pattern=r".+@example\.+.$")
    age : int = Field()
    date_of_birth : date = Field()
    profile : Profile = Field(default=Profile.Buyer)
    account_status : bool = Field(default=True)


class UpdateUser(BaseModel):
    name : Optional[str] = None
    last_name : Optional[str] = None # Фамилия
    middle_name : Optional[str] = None # Отчество
    telephone : Optional[str] = None
    email : Optional[str] = None
#    email : Optional[str] = Field(pattern=r".+@example\.+.$")
    age : Optional[int] = None
    date_of_birth : Optional[date] = None
    profile : Optional[Profile] = None
    account_status : Optional[bool] = Field(default=True)

    class Config:
        from_attributes = True


class ResponseUser(BaseModel):
    id: int
    name : str
    login:str
#    password : str = Field(...,)
    last_name : Optional[str] = None
    middle_name : Optional[str] = None # Отчество
    telephone : Optional[str] = None
    email : Optional[str] = None
#    email : str
    age : Optional[int] = None
    date_of_birth : Optional[date] = None
    profile : Optional[Profile] = None
    account_status : Optional[bool] = True



class LoginUser(BaseModel):
    
    name: str = Field(..., min_length=2)
    password: str = Field(..., min_length=2)

    model_config = ConfigDict(
    json_schema_extra={
        "example": {
            "name": "johndoe",
            "password": "securepassword123"
        }
    }
)




