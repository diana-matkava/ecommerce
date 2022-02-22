import os
import sys
from flask import Blueprint, flash, render_template, request, session, url_for, redirect
from flask_login import login_user, login_required, logout_user, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from .forms import CustomerRegistrationForm, SellerRegistrationForm, LoginForm
from .models import Customer, Seller, Type, Category
from ecommerce.extentions import db
from ecommerce.settings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER_SELLER, UPLOAD_FOLDER_CUSTOMER

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(id):
    if not session['role']:
        return Customer.query.get(int(id))
    if session['role']:
        return Seller.query.get(int(id))


bp = Blueprint('auth', __name__, url_prefix='/auth')


def allowed_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            session['role'] = 0
            login_user(customer)
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
            type = Type.query.filter_by(id=form.busines_type.data).first()
            seller = Seller(
                email=form.email.data,
                password=generate_password_hash(form.pwd.data),
                role=1,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                company_name=form.company_name.data,
                country=form.country.data,
                busines_type=form.busines_type.data,
                phone=form.phone.data
            )
            for category in form.category.data:
                seller.category.append(Category.query.filter_by(id=int(category)).first())


            logo = request.files['logo']
            if logo and allowed_extension(logo.filename):
                path = os.path.join( UPLOAD_FOLDER_SELLER, secure_filename(logo.filename))
                logo.save(path)
                seller.logo = path
                


            db.session.add(seller)
            db.session.commit()
            session['role'] = 1
            login_user(seller)
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
            seller = Seller.query.filter_by(email=form.email.data).first()
            if customer:
                if check_password_hash(customer.password, form.pwd.data):
                    login_user(customer)
                    session['role'] = customer.role
                    return redirect(url_for('hello'))
                else:
                    flash('Username (or email) or password is invalid', 'denger')
            elif seller:
                if check_password_hash(seller.password, form.pwd.data):
                    login_user(seller)
                    session['role'] = seller.role
                    return redirect(url_for('hello'))
                else:
                    flash('Username (or email) or password is invalid', 'denger')
        except Exception as _ex:
            flash("User with such email or password doesn't exist", 'denger')
    return render_template('auth/registration.html', form=form, title='Login')


@bp.route('/logout', methods=('GET', ))
def logout():
    logout_user()
    return redirect(url_for('hello'))