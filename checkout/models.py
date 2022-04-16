import enum
import datetime
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from flask import flash
from ecommerce.extentions import db
from ecommerce.products.models import Product, Currency


products = Table('products', db.Model.metadata,
    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
    Column('promotion_id', Integer, ForeignKey('promotion.id'), primary_key=True))


coupons = Table('coupons', db.Model.metadata,
    Column('promotion_id', Integer, ForeignKey('promotion.id'), primary_key=True),
    Column('coupon_id', Integer, ForeignKey('coupon.id'), primary_key=True))



class CouponType(enum.Enum):
    single = 'Single'
    multiple = 'Multiple'

    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]
    
    def __str__(self):
        return self.name


class DiscountType(enum.Enum):
    fixed = 'Fixed'
    persent = 'Percent'

    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]
    
    def __str__(self):
        return self.name


class Promotion(db.Model):
    __tablename__ = 'promotion'
    # __table_args__ = {'extend_existing': True}
    id = Column(Integer(), primary_key=True)
    title = Column(String(255), nullable=True)
    description = Column(String(1255), nullable=True)
    
    discount_type = Column(db.Enum(DiscountType), default=DiscountType.persent, nullable=False)
    discount_value = Column(Integer())

    ''' SINGLE = one coupon code shared by all shoppers
        MULTIPLE = array of unique coupon codes, each designed for individual use '''
    coupon_type = Column(db.Enum(CouponType), default=CouponType.multiple, nullable=False)
    coupon = relationship(
        'Coupon', secondary=coupons, lazy='subquery',
        backref=db.backref('promotion_', lazy=True))

    currency_id = Column(Integer(), ForeignKey('currency.id'))
    currency = relationship(Currency, backref=db.backref('currency', uselist=False))

    products = relationship(
        Product, secondary=products, lazy='subquery',
        backref=db.backref('promotion', lazy=True))

    ''' Starting date. The date when you set the promotion to start.
        Is NULL for promotions that start immediately after they are
        created. '''
    start_day = Column(DateTime(), default=datetime.datetime.now(), nullable=True)


    ''' Ending date. The date when you set the promotion to end. Is
        NULL for promotions that you want active indefinitely. '''
    end_day = Column(DateTime(), nullable=True)


    ''' Selecting the instant discount option will auto-apply
        the discount for ALL the selected products for all shoppers,
        without the need to enter the discount coupon.  '''
    instant_discount = Column(Boolean(), default=False)
    active = Column(Boolean(), default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def count_products(self):
        return len(self.products)


class Coupon(db.Model):
    __tablename__ = 'coupon'
    id = Column(Integer(), primary_key=True)
    code = Column(String(18), default=str(uuid.uuid4())[:18].replace('-', ''))
    promotion_id = Column(Integer(), ForeignKey('promotion.id'))
    promotion = relationship(Promotion, backref=db.backref('promotion', uselist=False))
    active = Column(Boolean(), nullable=True, default=True)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as _ex:
            print(_ex)
            db.session.rollback()
        finally:
            db.session.close