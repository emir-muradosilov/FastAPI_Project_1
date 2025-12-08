from pydantic import BaseModel, field_validator, Field, ConfigDict 
from enum import Enum
from uuid import UUID, uuid4
from datetime import date
from typing import Optional



class Profile(Enum):
    Seller : str = 'Seller'
    Buyer : str = 'Buyer'

class UserBase(BaseModel):
#    id : UUID = uuid4() 
    name : str = Field(...,)
    password : str = Field(...,)
    last_name : str = Field() # Фамилия
    middle_name : str = Field() # Отчество
    telephone : str = Field()
    email : str = Field()
#    email : str = Field(pattern=r".+@example\.+.$")
    age : int = Field()
    date_of_birth : date = Field()
    profile : Profile = Field()

    model_config = ConfigDict(
        # Параметры конфигурации здесь
    ) 


@field_validator('date_of_birth')
@classmethod
def chek_valid_date(clc, date_of_birth: date):
    today = date.today()
    eighteen_years_ago = date(today.year - 18, today.month, today.day)
    if date_of_birth > eighteen_years_ago:
        raise ValueError("Employees must be at least 18 years old.")
    return date_of_birth


class CreateUser(UserBase):
    pass


class UpdateUser(UserBase):
    name : Optional[str]
    last_name : Optional[str]  # Фамилия
    middle_name : Optional[str]  # Отчество
    telephone : Optional[str]
    email : Optional[str]
#    email : Optional[str] = Field(pattern=r".+@example\.+.$")
    age : Optional[str]
    date_of_birth : Optional[date]
    profile : Optional[Profile]


class DeliteUser(UserBase):
    pass


class ResponseUser(UserBase):
    id : str = Field(...,)


class LoginUser(BaseModel):
    name: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)

    model_config = ConfigDict(
    json_schema_extra={
        "example": {
            "name": "johndoe",
            "password": "securepassword123"
        }
    }
)




