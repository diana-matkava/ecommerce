from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, InputRequired, Length, Regexp, EqualTo, ValidationError
from wtforms import HiddenField
from werkzeug.security import check_password_hash
from .models import Customer, Seller



class CustomerRegistrationForm(FlaskForm):
    img = StringField('Avatar')
    username = StringField('username', validators=[
        InputRequired(),
        Length(5, 20, message='Please provide a valid username'),
        Regexp(
            regex="^\w+$",
            message="Username must start with letter, cant not contain spaces, and other special characters, except underscores",
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

    def validate_email(self, email):
        if Customer.query.filter_by(email=email.data).first() or \
            Seller.query.filter_by(email=email.data).first():
            raise ValidationError('Email already taken')


class SellerRegistrationForm(FlaskForm):
    img = StringField('Company Logo')
    company_name = StringField(validators=[
        InputRequired(), Length(0, 50)
    ])
    description = StringField(validators=[Length(0, 1000)])
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

def get_user(form, email):
        customer = Customer.query.filter_by(email=email.data).first()
        seller = Seller.query.filter_by(email=email.data).first()
        users = list(filter(None, [customer, seller]))
        print(users)
        if users:
            if len(users) == 1:
                form.user = users[0]
                print(form.user)
            else:
                raise ValidationError('Internal Server Error: Connect with service center')
        else:
            raise ValidationError('Email was not found')

def validate_password(form, pwd):
    if form.user.__dict__.get('email', False) \
        and not check_password_hash(form.user.password, pwd.data):
        raise ValidationError('Password is incorrect')



class LoginForm(FlaskForm):
    email = StringField('email', validators=[
        InputRequired(), Email(), get_user
        ])
    pwd = PasswordField(
        validators=[InputRequired(), validate_password]
    )
    user = HiddenField("User")

