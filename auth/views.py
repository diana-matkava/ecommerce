import os
import json
import requests
import pycountry
from pycountry import Currencies
from flask.json import jsonify
from flask import Blueprint, flash, render_template, request, session, url_for, redirect
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from ..products.models import Currency
from .forms import CustomerRegistrationForm, SellerRegistrationForm, LoginForm
from .models import Customer, Seller
from ..extentions import db
from ..settings import UPLOAD_FOLDER
from ..utils import allowed_extension
from werkzeug.datastructures import ImmutableMultiDict


login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(id):
    if not session['role']:
        return Customer.query.get(int(id))
    if session['role'] > 0:
        return Seller.query.get(int(id))


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login_default/<user>', methods=(['GET']))
def login_default(user):

    return redirect(url_for('home'))


@bp.route('/register_customer', methods=(['GET', 'POST']))
def register_customer():
    country = pycountry.countries.get(alpha_2='DE')
    c = Currencies.get(number=country.)

    if not session.get('country_code', False):
        ip = request.headers.get('X-Forwarded-For', False)
        if ip:
            URL = f'https://ipapi.co/{ip}/json'
            res = requests.get(URL)
            session['country_code'] = json.loads(res.text)['country_code']
        else:
            session['country_code'] = 'DE'

    if request.method == "POST":
        data = ImmutableMultiDict(request.form)
        form_data = data.to_dict(flat=True)
        form = CustomerRegistrationForm(**form_data)
        if form.validate_on_submit():
            try:
                customer = Customer(
                    username=form.username.data,
                    email=form.email.data,
                    password=generate_password_hash(form.pwd.data),
                    role=0
                )
                avatar = form.img.data
                if avatar and allowed_extension(avatar.filename):
                    path = os.path.join(
                        UPLOAD_FOLDER,
                        'img/user_inputs/customer_avatar/',
                        secure_filename(avatar.filename)
                    )
                    avatar.save(os.path.join(path))
                    customer.avatar = os.path.join(
                        'img/user_inputs/customer_avatar/',
                        secure_filename(avatar.filename)
                    )
                db.session.add(customer)
                db.session.commit()
                session['role'] = 0
                login_user(customer)
                flash(f'User {customer} was created successfully!')
                return redirect(url_for('home'))
            except Exception as _ex:
                flash(_ex, 'danger')
        else:
            valid_field = set(set(form_data.keys())).difference(form.errors.keys())
            data = form.errors
            data.update(dict.fromkeys(valid_field, ''))
            return jsonify(data)
    else:
        form = CustomerRegistrationForm()
    return render_template('auth/register.html', form=form, title='Sing Up')


@bp.route('/register_seller', methods=('GET', 'POST'))
def register_seller():
    if request.method == "POST":
        data = ImmutableMultiDict(request.form)
        form_data = data.to_dict(flat=True)
        form = SellerRegistrationForm(**form_data)
        if form.validate_on_submit():
            try:
                seller = Seller(
                    company_name=form.company_name.data,
                    email=form.email.data,
                    password=generate_password_hash(form.pwd.data),
                    role=1,
                    )

                logo = request.files['logo']
                if logo and allowed_extension(logo.filename):
                    path = os.path.join(UPLOAD_FOLDER, 'img/user_inputs/seller_logo/', secure_filename(logo.filename))
                    logo.save(path)
                    seller.logo =  os.path.join('img/user_inputs/seller_logo/', secure_filename(logo.filename))

                db.session.add(seller)
                db.session.commit()
                session['role'] = 1
                login_user(seller)
                flash(f'Seller {seller} was created successfully')
                return redirect(url_for('home'))
            except Exception as _ex:
                flash(_ex, 'danger')
        else:
            valid_field = set(set(form_data.keys())).difference(form.errors.keys())
            data = form.errors
            data.update(dict.fromkeys(valid_field, ''))
            return jsonify(data)
    else:
        form = SellerRegistrationForm()
    return render_template('auth/register.html', form=form, title='Register as Seller')

@login_required
@bp.route('/profile', methods=('GET', ))
def profile():
    if current_user.role:
        return render_template('auth/profile_seller.html', user=current_user)
    return render_template('auth/profile_customer.html', user=current_user)


@login_required
@bp.route('/edit_customer_profile', methods=('GET', 'POST', 'PUT'))
def edit_customer_profile():
    session.pop('_flashes', None)
    if request.method == 'POST':
        user = Customer.query.get(current_user.id)
        user.username = request.form.get('username')

        email = request.form.get('email')
        if not Seller.query.filter_by(email=email).first() and \
            not Customer.query.filter_by(email=email).first() and \
                user.email != email:
            user.email = request.form.get('email')
        elif user.email == email:
            user.email = request.form.get('email')
        else:
            flash('This email already taken')
            return redirect(url_for('auth.edit_seller_profile'))

        avatar = request.files['avatar']
        if avatar and avatar != user.avatar:
            if avatar and allowed_extension(avatar.filename):
                path = os.path.join(UPLOAD_FOLDER, 'img/user_inputs/customer_avatar/', secure_filename(avatar.filename))
                avatar.save(os.path.join(path))
                user.avatar = os.path.join('img/user_inputs/customer_avatar/', secure_filename(avatar.filename))
        current_pwd = request.form.get('password')
        if current_pwd:
            if check_password_hash(user.password, current_pwd):
                new_password = request.form.get('new_password')
                repeat_password = request.form.get('repeat_password')
                if new_password == repeat_password:
                    if len(new_password) >= 8:
                        user.password = generate_password_hash(new_password)
                    else:
                        flash(f'Password should contain more then 8 letters')
                        return redirect(url_for('auth.edit_seller_profile'))
                else:
                    flash('Password mismutch')
                    return redirect(url_for('auth.edit_seller_profile'))
            else:
                flash(f'Current password is incorrect')
                return redirect(url_for('auth.edit_seller_profile'))

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.profile'))
    return render_template('auth/edit_customer_profile.html', user=current_user)


@login_required
@bp.route('/edit_seller_profile', methods=('GET', 'POST'))
def edit_seller_profile():
    session.pop('_flashes', None)
    user = current_user
    data = {
        'user': current_user,
    }
    if request.method == 'POST':
        user.company_name = request.form.get('company_name')
        email = request.form.get('email')
        if not Seller.query.filter_by(email=email).first() and \
            not Customer.query.filter_by(email=email).first() and \
                user.email != email:
            user.email = request.form.get('email')
        elif user.email == email:
            user.email = request.form.get('email')
        else:
            flash('This email already taken')
            return redirect(url_for('auth.edit_seller_profile'))

        logo = request.files['logo']
        if logo and logo != user.logo:
            if logo and allowed_extension(logo.filename):
                path = os.path.join(UPLOAD_FOLDER, 'img/user_inputs/customer_avatar/', secure_filename(logo.filename))
                logo.save(os.path.join(path))
                user.logo = os.path.join('img/user_inputs/customer_avatar/', secure_filename(logo.filename))

        current_pwd = request.form.get('password')
        if current_pwd:
            if check_password_hash(user.password, current_pwd):
                new_password = request.form.get('new_password')
                repeat_password = request.form.get('repeat_password')
                if new_password == repeat_password:
                    if len(new_password) >= 8:
                        user.password = generate_password_hash(new_password)
                    else:
                        flash(f'Password should contain more then 8 letters')
                        return redirect(url_for('auth.edit_seller_profile'))
                else:
                    flash('Password mismutch')
                    return redirect(url_for('auth.edit_seller_profile'))
            else:
                flash(f'Current password is incorrect')
                return redirect(url_for('auth.edit_seller_profile'))

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.profile'))
    return render_template('auth/edit_seller_profile.html', **data)

@bp.route('/login', methods=('GET', 'POST'), strict_slashes=False)
def login():
    session.pop('_flashes', None)
    form = LoginForm()
    if form.validate_on_submit():
        try:
            customer = Customer.query.filter_by(email=form.email.data).first()
            seller = Seller.query.filter_by(email=form.email.data).first()
            if customer:
                if check_password_hash(customer.password, form.pwd.data):
                    login_user(customer)
                    session['role'] = customer.role
                    return redirect(url_for('home'))
                else:
                    flash('Username (or email) or password is invalid', 'denger')
            elif seller:
                if check_password_hash(seller.password, form.pwd.data):
                    login_user(seller)
                    session['role'] = seller.role
                    return redirect(url_for('home'))
                else:
                    flash('Username (or email) or password is invalid', 'denger')
        except Exception as _ex:
            flash("User with such email or password doesn't exist", 'denger')
    return render_template('auth/registration.html', form=form, title='Login')


@bp.route('/logout', methods=('GET', ))
def logout():
    logout_user()
    return redirect(url_for('home'))


@bp.route('/delete_customer/<id>', methods=['GET', 'POST', 'DELETE'])
def delete_customer(id):
    Customer.query.get(id).delete()
    return redirect(url_for('home'))


@bp.route('/delete_seller/<id>', methods=['GET', 'POST', 'DELETE'])
def delete_seller(id):
    Seller.query.get(id).delete()
    return redirect(url_for('home'))


@login_required
@bp.route('/change_currency', methods=['POST'])
def change_currency():
    currency = request.form.get('currency')
    current_user.display_currency_id = Currency.query.filter_by(abr=currency)[0].id
    db.session.add(current_user)
    db.session.commit()
    return ('', 204)

@bp.route('/createsupeuser', methods=['POST'])
def create_superuser(id):
    load_user(id)
    return ('', 204)
