from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey,Column, String
import enum
from typing import List
from datetime import date
from sqlalchemy import Enum
import datetime
from datetime import datetime, timedelta
from enum import Enum as PyEnum


class Base(DeclarativeBase):
    pass


class Profile(enum.Enum):
    Seller = 'Seller'
    Buyer = 'Buyer'


class User(Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column()
    last_name : Mapped[str] = mapped_column(nullable=True) # Фамилия
    middle_name : Mapped[str] = mapped_column(nullable=True) # Отчество
    telephone : Mapped[str] = mapped_column(nullable=True)
    email : Mapped[str] = mapped_column(nullable=True)
    password : Mapped[str] = mapped_column(nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    date_of_birth : Mapped[date] = mapped_column(nullable=True)
    profile : Mapped[Profile] = mapped_column(Enum(Profile), nullable=True, default='Buyer')
    
    # Python связь
    cart: Mapped[List["Cart"]] = relationship(back_populates="user")
    token : Mapped['Token'] = relationship(back_populates='user')


class Category(Base):
    __tablename__ = 'category'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column()
    description : Mapped[str] = mapped_column()
    img : Mapped[str] = mapped_column()
    slug : Mapped[str] = mapped_column()
    # Python связь
    products: Mapped[List["Product"]] = relationship(back_populates="category")

class Size(enum.Enum):
    length = 'length'
    width ='width'
    height = 'height'
    weight = 'weight'

class Color(enum.Enum):
    red = 'Red'
    orange = 'Orange'
    yellow = 'Yellow'
    green = 'Green'
    blue = 'Blue'
    purple = 'Purple'
    gradient = 'Gradient'
    multicolor = 'Multicolor'



class Product(Base):
    __tablename__ = 'products'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column()
    description : Mapped[str] = mapped_column()
    text : Mapped[str] = mapped_column()
    img : Mapped[str] = mapped_column()
    slug : Mapped[str] = mapped_column()
    coast : Mapped[float] = mapped_column()
    quantity : Mapped[int] = mapped_column()
    size: Mapped[str] = mapped_column(String(20), nullable=True)
    color: Mapped[str] = mapped_column(String(20), nullable=True)
    # Внешний ключ
    category_id : Mapped[int] = mapped_column(ForeignKey('category.id'))
    # Python связь
    gallery: Mapped[List["Gallery"]] = relationship(back_populates="product")
    cart: Mapped[List["Cart"]] = relationship(back_populates="product")
    category = relationship("Category", back_populates="products")


class Gallery(Base):
    __tablename__ = 'gallery'
    id : Mapped[int] = mapped_column(primary_key=True)
    # Внешний ключ
    product_id : Mapped[int] = mapped_column(ForeignKey('products.id'))
    # Python связь
    product: Mapped["Product"] = relationship(back_populates="gallery")



class Cart(Base):
    __tablename__ = 'cart'
    id : Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(default=1)  # Количество товара в корзине
    # Внешний ключ
    product_id : Mapped[int] = mapped_column(ForeignKey('products.id'))
    user_id : Mapped[int] = mapped_column(ForeignKey('users.id'))
    # Python связь
    product: Mapped["Product"] = relationship(back_populates="cart")
    user: Mapped["User"] = relationship(back_populates="cart")


class Token(Base):
    __tablename__='token'
    id : Mapped[int] = mapped_column(primary_key=True)
    token : Mapped[str] = mapped_column(nullable=False)
    user_id : Mapped['int'] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='token')


'''
{
"name": "dsdsdsd",
"password": "sdsadadas",
"last_name": "sdsadadas",
"middle_name": "sdsadadas",
"telephone": "sdsadadas",
"email": "sdsa.dad@as.ru",
"age": 15,
"date_of_birth": "1993-09-12",
"profile": "Seller"
}
'''

