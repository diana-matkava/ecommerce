from flask_login import UserMixin
from sqlalchemy_utils import PhoneNumberType

import sqlalchemy.types as types
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ecommerce.extentions import db


categories = db.Table('categories', db.Model.metadata,
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True),
    Column('seller_id', Integer, ForeignKey('seller.id'), primary_key=True)
)


class User(UserMixin):
    __abstract__ = True
    R_CUSTOMER = 0
    R_SELLER = 1
    id = Column(Integer(), primary_key=True)
    email = Column(String(125), unique=True, nullable=False)
    password = Column(String(125), nullable=False)
    role = Column(Integer, nullable=False, default=R_CUSTOMER)


class Customer(User, db.Model):
    username = Column(String(50), nullable=False)
    avatar = Column(Integer, ForeignKey('customer_avatar.id'))

    def __repr__(self):
        return f'{self.username}'


class Seller(User, db.Model):
    first_name = Column(String(50))
    last_name = Column(String(50))
    company_name = Column(String(125), nullable=False)
    country = Column(String(125), nullable=False)
    category = relationship(
        'Category', secondary=categories, lazy='subquery',
        backref=db.backref('seller', lazy=True)
        )
    busines_type = relationship("Type", backref="busines_type", lazy=True)
    phone = Column(PhoneNumberType(), nullable=False)
    logo = Column(Integer, ForeignKey('company_logo.id'), nullable=True)


    def __repr__(self):
        return f'{self.company_name}'


class CustomerAvatar(db.Model):
    id = Column(Integer(), primary_key=True)
    path = Column(String(125), nullable=False)


class CompanyLogo(db.Model):
    id = Column(Integer, primary_key=True)
    path = Column(String(125), nullable=False)


class Type(db.Model):
    id = Column(Integer(), primary_key=True)
    seller_id = Column(Integer, ForeignKey('seller.id'))
    name = Column(String(125), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.name}'


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.name}'
