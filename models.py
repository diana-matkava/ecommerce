from flask_login import UserMixin

import sqlalchemy.types as types
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from __init__ import db


class ChoiceType(types.TypeDecorator):
    impl = types.String

    def __init__(self, choices, **kwargs):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        return [key for key, val in self.choices.iteritems() if val == value][0]

    def precess_result_value(self, value, dialect):
        return self.choices[value]


class User(db.Model):
    __abstract__ = True
    R_CUSTOMER = 0
    R_SELLER = 1

    email = Column(String(125), unique=True, nullable=False)
    password = Column(String(125), nullable=False)
    role = Column(Integer, nullable=False, default=R_CUSTOMER)


class Customer(User, UserMixin):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(50), nullable=False)
    avatar = relationship('CustomerAvatar', backref='customer', lazy=True)

    def __repr__(self):
        return self.nickname


class Seller(User, UserMixin):
    T_TYPE = {
            'sole proprietorship': 'sole proprietorship',
            'partnership': 'partnership',
            'small corporation': 'small corporation',
            'corporation': 'corporations'
        }
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    company_name = Column(String(125), nullable=False)
    country = Column(String(125), nullable=False)
    type = Column(String(125), nullable=False)
    phone = Column(String(12), nullable=False)
    logo = relationship('CompanyLogo', backref='seller', lazy=True)

    def __repr__(self):
        return self.company_name


class CustomerAvatar(db.Model):
    id = Column(Integer, primary_key=True)
    avatar = Column(String(125), nullable=False)
    customer = Column(Integer, ForeignKey('customer.id'))


class CompanyLogo(db.Model):
    id = Column(Integer, primary_key=True)
    logo = Column(String(125), nullable=False)
    seller = Column(Integer, ForeignKey('seller.id'))


