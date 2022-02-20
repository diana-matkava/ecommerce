from ast import Eq
from curses.ascii import EM
from operator import le
import pwd
from string import capwords
from unittest.loader import VALID_MODULE_NAME
from flask_wtf import FlaskForm
from .models import Customer, Seller
from wtforms import StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired, Length, Regexp, EqualTo, ValidationError



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
    # submit = SubmitField("Submit")


    def validate_email(self, email):
        if Customer.query.filter_by(email=email.data).first():
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
    country = StringField('Country', validators=[
        InputRequired(), Length(0, 20)
    ])
    type = StringField('Business type', validators=[
        InputRequired()
    ])
    logo = StringField('Company Logo')
    phone = StringField('Phone', validators=[
        InputRequired()
    ])
    email = StringField('Email', validators=[
        InputRequired(), Email()
    ])
    pwd = PasswordField('Password', validators=[
        InputRequired(), 
        Length(8, 50, message='Password should be 8 or more characters')
    ])
    cpwd = PasswordField('Confirm password', validators=[
        InputRequired(), EqualTo('pwd', message='Password should match')
    ])

    def validate_email(self, email):
        if Seller.query.filter_by(email=email.data).first():
            raise ValidationError('Email already taken')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[
        InputRequired(), Email()
        ])
    pwd = PasswordField(validators=[InputRequired()])
