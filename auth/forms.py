import pycountry
from flask_wtf import FlaskForm
from wtforms_alchemy import PhoneNumberField
from wtforms import StringField, PasswordField, validators, SelectMultipleField, SelectField
from wtforms.validators import Email, InputRequired, Length, Regexp, EqualTo, ValidationError
from .models import Category, Customer, Seller, Type



class CustomerRegistrationForm(FlaskForm):
    username = StringField('username', validators=[
        InputRequired(),
        Length(5, 20, message='Please provide a valid usename'),
        Regexp(
            "^[A-Za-z][A-Za-z0-9_.]*$",
            0,
            "Username must have only letters, " "numbers, dots or underscores",
        )
    ])
    email = StringField('email', validators=[InputRequired(), Email(), Length(5, 20)])
    pwd = PasswordField('password', validators=[
        InputRequired(),
        Length(8, 20, message='Password should be 8 or more characters')
    ])
    cpwd = PasswordField('confirm_password', validators=[
        InputRequired(),
        Length(8, 20),
        EqualTo('pwd', message='Password must match')
    ])
    avatar = StringField('Avatar')


    def validate_email(self, email):
        if Customer.query.filter_by(email=email.data).first() or \
            Seller.query.filter_by(email=email.data).first():
            raise ValidationError('Email already taken')


class SellerRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        InputRequired(), Length(0, 20), Regexp(
            "^[A-Za-z][A-Za-z0-9_.]*$",
            0,
            "First name must have only letters, " "numbers, dots or underscores"
        )
    ])
    last_name = StringField('First Name', validators=[
        InputRequired(), Length(0, 20), Regexp(
            "^[A-Za-z][A-Za-z0-9_.]*$",
            0,
            "First name must have only letters, " "numbers, dots or underscores"
        )
    ])
    company_name = StringField(validators=[
        InputRequired(), Length(0, 50)
    ])
    country = SelectField('Country', validate_choice=False)
    busines_type = SelectField('Business type:', validate_choice=False)
    category = SelectMultipleField('Products category:', validate_choice=False)
    logo = StringField('Company Logo')
    # phone = PhoneNumberField('Phone', validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    pwd = PasswordField('Password', validators=[
        InputRequired(),
        Length(8, 50,
        message='Password should be 8 or more characters')
    ])
    cpwd = PasswordField('Confirm password', validators=[
        InputRequired(),
        EqualTo('pwd', message='Password should match')
    ])

    def validate_email(self, email):
        if Seller.query.filter_by(email=email.data).first() or \
        Customer.query.filter_by(email=email.data).first():
            raise ValidationError('Email already taken')

    def __init__(self, *args, **kwargs):
        super(SellerRegistrationForm, self).__init__(*args, **kwargs)
        self.busines_type.choices = [(a.id, a.name) for a in Type.query.order_by(Type.name)]
        self.category.choices = [(a.id, a.name) for a in Category.query.order_by(Category.name)]
        self.country.choices = [(a.alpha_2, a.name) for a in pycountry.countries]


class LoginForm(FlaskForm):
    email = StringField('email', validators=[
        InputRequired(), Email()
        ])
    pwd = PasswordField(validators=[InputRequired()])
