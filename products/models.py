import datetime
import requests
import bs4
from flask_login import current_user
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from flask import session
from ..extentions import db
from ..settings import CURRENCY_API_KEY

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



class Currency(db.Model):
    __tablename__ = 'currency'
    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    abr = Column(String(3))

    def __repr__(self):
        return self.abr


class Product(db.Model):
    id = Column(Integer(), primary_key=True)
    name = Column(String(225), nullable=False)
    description = Column(String(1500), nullable=True)
    images = relationship(
        'Image', secondary=images, lazy='subquery',
        backref=db.backref('product', lazy=True)
    )
    price = Column(Integer())
    currency_id = Column(Integer(), ForeignKey('currency.id'), nullable=True)
    currency = relationship(Currency, backref=db.backref('product_currency', uselist=False))
    quantity = Column(Integer())
    product_category = relationship(
        'ProductCategory', secondary=product_categories, lazy='subquery',
        backref=db.backref('product', lazy=True)
    )

    owner = Column(String(225), nullable=True)
    owner_name = Column(String(225), nullable=True)
    like = Column(Integer(), default=0, nullable=True)
    created = Column(DateTime(), default=datetime.datetime.now(), nullable=True)

    def get_price(self):
        price = self.price
        if current_user.is_authenticated and current_user.display_currency_id != self.currency_id:
            cur_pair = ' '.join(['RATE', self.currency.abr, current_user.currency.abr])
            if cur_pair not in session:
                url = requests.get(f'https://www.xe.com/currencyconverter/convert/?Amount=1&From={self.currency.abr}&To={current_user.currency.abr}')
                soup = bs4.BeautifulSoup( url.text, "html.parser" )
                rate = float(soup.find( "p" , class_='result__BigRate-sc-1bsijpp-1 iGrAod' ).text.split(' ')[0])
                session[cur_pair] = rate
            else:
                rate = session[cur_pair]
            price = self.price * rate
        return float(round(price, 2))


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
            cur_pair = ' '.join(['RATE', order.product_obj.currency.abr, current_user.currency.abr])
            if current_user.display_currency_id == order.product_obj.currency_id:
                price += order.product_obj.price * order.quantity
            else:
                rate = session[cur_pair]
                price += order.product_obj.price * order.quantity * rate

        return float(round(price, 2))
    
    def price_with_discount(self):
        price, total_price = 0, 0
        for order in self.product_order:
            cur_pair = ' '.join(['RATE', order.product_obj.currency.abr, current_user.currency.abr])
            if current_user and current_user.active_discount:
                discount_type = current_user.coupons[-1].promotion.discount_type.name 
                discount_value = current_user.coupons[-1].promotion.discount_value
                discount_products = current_user.coupons[-1].promotion.products

                if order.product_obj in discount_products:
                    if discount_type == 'fixed':
                        if order.product_obj.price >= discount_value:
                            price += (order.product_obj.price - discount_value) * order.quantity
                        else:
                            price += order.product_obj.price * order.quantity
                    elif discount_type == 'persent':
                        price += order.product_obj.price * (1-(discount_value / 100)) * order.quantity
                else:
                    price += order.product_obj.price * order.quantity
                
                total_price += price
                

                if current_user.display_currency_id != order.product_obj.currency_id:
                    rate = session[cur_pair]
                    total_price -= price
                    total_price = price * rate
                
                price = 0
        return float(round(total_price, 2))


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

    def get_price(self, disc=True):
        price = None
        cur_pair = ' '.join(['RATE', self.product_obj.currency.abr, current_user.currency.abr])
        if current_user and current_user.display_currency_id != self.product_obj.currency_id:
            if cur_pair not in session:
                url = requests.get(f'https://www.xe.com/currencyconverter/convert/?Amount=1&From={self.product_obj.currency}&To={current_user.currency.abr}')
                soup = bs4.BeautifulSoup( url.text, "html.parser" )
                rate = float(soup.find( "p" , class_='result__BigRate-sc-1bsijpp-1 iGrAod' ).text.split(' ')[0])
                session[cur_pair] = rate
            else:
                rate = session[cur_pair]
            
            price = self.product_obj.price * rate

        discount_products = current_user.coupons[-1].promotion.products
        if self.product_obj in discount_products and disc:
            discount_type = current_user.coupons[-1].promotion.discount_type.name 
            discount_value = current_user.coupons[-1].promotion.discount_value
            if discount_type == 'fixed':
                if self.product_obj.price >= discount_value:
                    price = price - discount_value
                else:
                    price = price
            elif discount_type == 'persent':
                price = price * (1-(discount_value / 100))

        return float(round(price, 2)) if price else None


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
