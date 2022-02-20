from flask import Blueprint, flash, render_template, request, session, url_for, redirect
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import CustomerRegistrationForm, SellerRegistrationForm, LoginForm
from .models import Customer, Seller
from ecommerce.extentions import db

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(id):
    return Customer.query.get(int(id))


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/registration_customer', methods=('GET', 'POST'), strict_slashes=False)
def registrate_customer():
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        try:
            customer = Customer(
                username=form.username.data, 
                email=form.email.data,
                password=generate_password_hash(form.pwd.data),
                role=0
            )
            db.session.add(customer)
            db.session.commit()
            flash(f'User {customer} was created successfully!')
            return redirect(url_for('hello'))
        except Exception as _ex:
            flash(_ex, 'denger')
    return render_template('auth/registration.html', form=form, title='Sing Up')


@bp.route('/registration_seller', methods=('GET', 'POST'))
def registrate_seller():
    form = SellerRegistrationForm()
    if form.validate_on_submit():
        try:
            seller = Seller(
                email=form.email.data,
                password=form.pwd.data,
                role=1,

                first_name=form.first_name.data,
                last_name=form.last_name.data,
                company_name=form.company_name.data,
                country=form.country.data,
                type=form.type.data,
                phone=form.phone.data
            )
            db.session.add(seller)
            db.session.commit()
            flash(f'Seller {seller} was created successfully')
            return redirect(url_for('hello'))
        except Exception as _ex:
            flash(_ex, 'denger')
    return render_template('auth/registration_seller.html', form=form, title='Register as Seller')


@bp.route('/login', methods=('GET', 'POST'), strict_slashes=False)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            customer = Customer.query.filter_by(email=form.email.data).first()
            if check_password_hash(customer.password, form.pwd.data):
                login_user(customer)
                return redirect(url_for('hello'))
            else:
                flash('Username (or email) or password is invalid', 'light')
        except Exception as _ex:
            flash(_ex, 'denger')
    return render_template('auth/registration.html', form=form, title='Login')


@bp.route('/logout', methods=('GET', ))
def logout():
    logout_user()
    return redirect(url_for('hello'))