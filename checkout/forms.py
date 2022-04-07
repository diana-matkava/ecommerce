from locale import currency
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SelectMultipleField, SelectField, BooleanField, IntegerField, DateTimeField, DateField
from wtforms.validators import InputRequired, Length, ValidationError
from ecommerce.checkout.models import Promotion, Coupon, DiscountType, CouponType, Currency
from ecommerce.products.models import Product


class PromotionForm(FlaskForm):
	title = StringField('Title', validators=[
		Length(0, 225, message='Please input valid title'), InputRequired()])
	description = StringField('Description', validators=[
		Length(0, 1124, message='Please input valid description')])
	discount_type = SelectField('Discount type', validate_choice=False, 
		validators=[InputRequired()])
	discount_value = IntegerField('Discount value')
	coupon_type = SelectField('Coupon type', validate_choice=False, render_kw={'id': 'm_select'})
	currency = SelectField('Currency', validate_choice=False)
	products = SelectMultipleField('Apply discount for: ', validate_choice=False, 
		render_kw={'style':'height: 250px'})
	start_day = DateField('Start in')
	end_day = DateField('End in')
	instant_discount = BooleanField('Apply instantly for every selected products')
	active = BooleanField()


	def __init__(self, *args, **kwargs):
		super(PromotionForm, self).__init__(*args, **kwargs)
		self.discount_type.choices =DiscountType.choices()
		self.coupon_type.choices = CouponType.choices()
		self.currency.choices = [
			(currency.id, currency.abr) for currency in Currency.query.all()]
		self.products.choices = [
			(product.id, product.name) for product in Product.query.filter_by(owner=current_user.email).order_by(Product.created)]


