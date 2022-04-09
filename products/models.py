from ast import For
import datetime
from flask_login import current_user
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from ecommerce.extentions import db

images = db.Table('product_images', db.Model.metadata, 
    Column('image_id', Integer, ForeignKey('image.id'), primary_key=True), 
    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True)
)

product_categories = db.Table('product_categories', db.Model.metadata,
    Column('product_category_id', Integer, ForeignKey('product_category.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True)
)

orders = db.Table('orders', db.Model.metadata, 
    Column('card_id', Integer, ForeignKey('card.id'), primary_key=True),
    Column('order_id', Integer, ForeignKey('order.id'), primary_key=True))


class Product(db.Model):
    id = Column(Integer(), primary_key=True)
    name = Column(String(225), nullable=False)
    description = Column(String(1500), nullable=True)
    images = relationship(
        'Image', secondary=images, lazy='subquery',
        backref=db.backref('product', lazy=True)
    )
    price = Column(Integer())
    quantity = Column(Integer())
    product_category = relationship(
        'ProductCategory', secondary=product_categories, lazy='subquery',
        backref=db.backref('product', lazy=True)
    )

    owner = Column(String(225), nullable=True)
    owner_name = Column(String(225), nullable=True)
    like = Column(Integer(), default=0, nullable=True)
    created = Column(DateTime(), default=datetime.datetime.now(), nullable=True)


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()


class Card(db.Model):
    __tablename__ = 'card'

    id = Column(Integer(), primary_key=True)
    product_order = relationship('Order', secondary=orders, lazy='subquery',
                backref=db.backref('card', lazy=True))
    customer = Column(String(225), nullable=False)
    promo = Column(Integer())

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as _ex:
            print(_ex)
            db.session.rollback()
        finally:
            db.session.close
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_quantity(self):
        quantity = 0
        for order in self.product_order:
            quantity += order.quantity
        return quantity

    def get_total_price(self):
        price = 0
        for order in self.product_order:
            price += order.product_obj.price * order.quantity
        return price
    
    def price_with_discount(self):
        price = 0
        for order in self.product_order:
            if current_user.active_discount:
                discount_type = current_user.coupons[-1].promotion.discount_type.name 
                discount_value = current_user.coupons[-1].promotion.discount_value
                discount_products = current_user.coupons[-1].promotion.products

                if order.product_obj in discount_products:
                    if discount_type == 'fixed':
                        if self.product_obj.price >= discount_value:
                            price += order.product_obj.price - discount_value * order.quantity
                    else:
                        price += order.product_obj.price * (1-(discount_value / 100)) * order.quantity
                else:
                    price += order.product_obj.price * order.quantity
        return price


class Order(db.Model):
    __tablename__ = 'order'
    id = Column(Integer(), primary_key=True)
    product = Column(Integer(), ForeignKey('product.id'), nullable=True)
    product_obj = db.relationship("Product", backref=db.backref("product", uselist=False))
    quantity = Column(Integer, nullable=False)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as _ex:
            print(_ex)
            db.session.rollback()
        finally:
            db.session.close

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_price(self):
        if current_user.active_discount:
            if current_user.coupons[-1].promotion.discount_type.name == 'fixed':
                if self.product_obj.price >= current_user.coupons.promotion.discount_value:
                    price = self.product_obj.price - current_user.coupons.promotion.discount_value
            else:
                price = self.product_obj.price * current_user.coupons.promotion.discount_value // 100
        else:
            price = self.product_obj.price
        return price


class Image(db.Model):
    __tablename__ = 'image'

    id = Column(Integer(), primary_key=True)
    path = Column(String(225), nullable=False)


class ProductCategory(db.Model):
    __tablename__ = 'product_category'

    id = Column(Integer(), primary_key=True)
    name = Column(String(225), nullable=False)

    def __repr__(self):
        return f'{self.name}'
