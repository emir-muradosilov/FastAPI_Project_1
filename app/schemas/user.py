from pydantic import EmailStr, BaseModel, field_validator, Field, ConfigDict 
from enum import Enum
from uuid import UUID, uuid4
from datetime import date
from typing import Optional



class Profile(Enum):
    Seller : str = 'Seller'
    Bayer : str = 'Bayer'

class UserBase(BaseModel):
    id : UUID = uuid4() 
    name : str = Field(...,)
    last_name : str = Field(...,) # Фамилия
    middle_name : str = Field(...,) # Отчество
    telephone : str = Field(...,)
    email : EmailStr = Field(..., pattern=r".+@example\.+.$")
    age : int = Field(...,)
    date_of_birth : date = Field(...,)
    profile : Profile = Field(...,)

    model_config = ConfigDict(
        # Параметры конфигурации здесь
    ) 


@field_validator('date')
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
    email : Optional[EmailStr] = Field(pattern=r".+@example\.+.$")
    age : Optional[str]
    date_of_birth : Optional[date]
    profile : Optional[Profile]


class DeliteUser(UserBase):
    id : UUID = uuid4()


class ResponseUser(UserBase):
    id : UUID = uuid4()


