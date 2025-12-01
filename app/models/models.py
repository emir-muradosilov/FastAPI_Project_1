from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey,Column, String
import enum
from typing import List
from datetime import date
from sqlalchemy import Enum

class Base(DeclarativeBase):
    pass


class Profile(enum.Enum):
    Seller = 'Seller'
    Buyer = 'Buyer'


class User(Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column()
    last_name : Mapped[str] = mapped_column() # Фамилия
    middle_name : Mapped[str] = mapped_column() # Отчество
    telephone : Mapped[str] = mapped_column()
    email : Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()
    date_of_birth : Mapped[date] = mapped_column()
    profile : Mapped[Profile] = mapped_column(Enum(Profile))
    # Python связь
    cart: Mapped[List["Cart"]] = relationship(back_populates="user")


class Category(Base):
    __tablename__ = 'category'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column()
    description : Mapped[str] = mapped_column()
    img : Mapped[str] = mapped_column()
    slug : Mapped[str] = mapped_column()
    # Python связь
    product: Mapped[List["Product"]] = relationship(back_populates="category")

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
    size : Mapped[Size] = mapped_column(Enum(Size))
    color : Mapped[Color] = mapped_column(Enum(Size))
    # Внешний ключ
    category_id : Mapped[int] = mapped_column(ForeignKey('category.id'))
    # Python связь
    gallery: Mapped[List["Gallery"]] = relationship(back_populates="product")
    cart: Mapped[List["Cart"]] = relationship(back_populates="product")


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


