from flask_wtf import FlaskForm
from wtforms import validators, SelectMultipleField, StringField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, Regexp
from wtforms.widgets import TextArea
from ..products.models import Product, Image, ProductCategory


class CreateProductForm(FlaskForm):
    name = StringField('Product title', validators=[
        InputRequired(), 
        Length(2, 225, message='Please provide a valid product name')
    ])
    description = StringField('Product description', widget=TextArea())
    price = IntegerField('Price')
    quantity = IntegerField('Quantity')

    image = StringField('Product images')
    category = SelectMultipleField('Select product categories: ', validate_choice=False)

    def __init__(self, *args, **kwargs):
        super(CreateProductForm, self).__init__(*args, **kwargs)
        self.category.choices = [(a.id, a.name) for a in ProductCategory.query.all()]
