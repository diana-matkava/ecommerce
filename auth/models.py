from xmlrpc.client import Boolean
from flask_login import UserMixin
# from sqlalchemy_utils.types.phone_number import PhoneNumber

import sqlalchemy.types as types
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from ..extentions import db
from ..products.models import Product, Currency
from ..checkout.models import Promotion, Coupon


categories = db.Table('categories', db.Model.metadata,
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True),
    Column('seller_id', Integer, ForeignKey('seller.id'), primary_key=True)
)

seller_likes = db.Table('seller_likes', db.Model.metadata, 
    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
    Column('seller_id', Integer, ForeignKey('seller.id'), primary_key=True)
)

customer_likes = db.Table('customer_likes', db.Model.metadata, 
    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
    Column('customer_id', Integer, ForeignKey('customer.id'), primary_key=True)
)

promotions = db.Table('promotions', db.Model.metadata, 
    Column('promotion_id', Integer, ForeignKey('promotion.id'), primary_key=True),
    Column('seller_id', Integer, ForeignKey('seller.id'), primary_key=True)
)

active_codes_for_custmr = db.Table('active_codes_for_custmr', db.Model.metadata, 
    Column('coupon_id', Integer, ForeignKey('coupon.id'), primary_key=True),
    Column('customer_id', Integer, ForeignKey('customer.id'), primary_key=True)    
)

active_codes_for_sel = db.Table('active_codes_for_sel', db.Model.metadata, 
    Column('coupon_id', Integer, ForeignKey('coupon.id'), primary_key=True),
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
    card_id = Column(Integer, nullable=True)
    active_discount = Column(Boolean, default=False, nullable=True)

    @declared_attr
    def display_currency_id(cls):
        return Column(Integer, ForeignKey('currency.id'), default=1)


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def like_product(self, id):
        product = Product.query.get(id)
        if product not in self.liked_products:
            self.liked_products.extend([product])
            product.like += 1
        else:
            self.liked_products.remove(product)
            product.like -= 1
        db.session.add(product)
        db.session.commit()


class Customer(User, db.Model):
    username = Column(String(50), nullable=False)
    avatar = Column(Integer, ForeignKey('customer_avatar.id'))
    liked_products = relationship('Product', secondary=customer_likes, 
        backref=db.backref('customer', lazy=True))
    coupons = relationship(Coupon, secondary=active_codes_for_custmr, lazy='subquery', 
                backref=db.backref('customer', lazy=True))
    currency = relationship(Currency, backref=db.backref('customer_currency', uselist=False))

    def __repr__(self):
        return f'{self.username}'
    

class Seller(User, db.Model):
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    company_name = Column(String(125), nullable=True)
    country = Column(String(125), nullable=True)
    category = relationship(
        'Category', secondary=categories, lazy='subquery',
        backref=db.backref('seller', lazy=True)
        )
    busines_type = relationship("Type", backref="busines_type", lazy=True)
    phone = Column(String(), nullable=True)
    logo = Column(Integer, ForeignKey('company_logo.id'), nullable=True)
    liked_products = relationship('Product', secondary=seller_likes, 
        backref=db.backref('seller', lazy=True))
    promotion = relationship(
        Promotion, secondary=promotions, lazy='subquery',
        backref=db.backref('seller', lazy=True))
    coupons = relationship(Coupon, secondary=active_codes_for_sel, lazy='subquery', 
                backref=db.backref('seller', lazy=True))
    currency = relationship(Currency, backref=db.backref('seller_currency', uselist=False))
    
    
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
