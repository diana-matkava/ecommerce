from ast import For
import datetime
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


cards = db.Table('cards', db.Model.metadata, 
    Column('card_id', Integer, ForeignKey('card.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True))

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
    like = Column(Integer(), default=0, nullable=True)
    created = Column(DateTime(), default=datetime.datetime.now(), nullable=True)

    def __repr__(self):
        return f'{self.name}'

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Card(db.Model):
    __tablename__ = 'card'

    id = Column(Integer(), primary_key=True)
    products = relationship('Product', secondary=cards, lazy='subquery',
                backref=db.backref('card', lazy=True))
    customer = Column(String(225), nullable=False)
    price = Column(Integer())
    promo = Column(Integer())


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
