from locale import currency
import sys
import uuid
import datetime
from xmlrpc.client import boolean
from ..checkout.models import Coupon, Currency, Promotion, DiscountType, CouponType
from ..products.models import Product
from ..extentions import db
from flask.json import jsonify
from flask_login import login_required
from flask import Blueprint, request, render_template, redirect, session, url_for, flash
from flask_login import current_user, login_required
from ..checkout.forms import PromotionForm


checkout = Blueprint('checkout', __name__, url_prefix='/checkout')
promotion = Blueprint('promotion', __name__, url_prefix='/promotion')


@login_required
@checkout.route('/marketing_tools', methods=['GET'])
def marketing_tools():
    data = dict()
    if current_user.promotion:
        data = {
            'promotions': current_user.promotion
        }
        
    return render_template('promotion/marketing_tools.html', **data)


@checkout.route('/create_promotion', methods=['GET', 'POST'])
def create_promotion():
    session.pop('_flashes', None)
    form = PromotionForm()
    form.products.data = [str(product.id) for product in Product.query.filter_by(owner=current_user.email)]
    today = datetime.datetime.now()
    data = {
        'form': form,
        'today': today
    }

    if request.method == 'POST':
        try:
            promotion = Promotion(
                title=request.form.get('title'),
                description=request.form.get('description'),
                discount_type=DiscountType[request.form.get('discount_type')],
                discount_value=int(request.form.get('discount_value')),
                coupon_type=CouponType[request.form.get('coupon_type')],
                currency_id=int(request.form.get('currency')),
                start_day=datetime.datetime.strptime(
                     request.form['start_day'][:-6],
                     '%Y-%m-%d'
                     ) if request.form.get('start_day') else None,
                end_day=datetime.datetime.strptime(
                     request.form['end_day'][:-6],
                     '%Y-%m-%d'
                     ) if request.form.get('end_day') else None,
                instant_discount=True if request.form.get('instant_discount') else False,
                active=True if request.form.get('active') else None
            )
            
            promotion.products.extend([Product.query.get(int(product)) for product in request.form.getlist('products')])

            promotion.save()
        
            coupons = request.form.get('coupons')
            if coupons:
                for coupon in coupons.splitlines():
                    coupon = Coupon(
                        code=coupon,
                        promotion_id=promotion.id
                    )
                    promotion.coupon.extend([coupon])

                    db.session.add(promotion)
                    db.session.add(coupon)
            else:
                
                coupon = Coupon(
                    code=str(uuid.uuid4())[:18].replace('-', ''),
                    promotion=promotion
                )
                promotion.coupon.extend([coupon])

                db.session.add(coupon)
                db.session.add(promotion)

            try:
                current_user.promotion.extend([promotion])
                db.session.add(current_user)
                db.session.commit()
                flash('Promotion added')
                return redirect(url_for('checkout.marketing_tools'))
            except Exception as _ex:
                flash(_ex)

        except Exception as _ex:
            flash(_ex)
        
    else:
        flash('Something went wrong')
    return render_template('promotion/create_promotion.html', **data)


@checkout.route('/generate_coupon', methods=['PUT'])
def generate_coupon():
    if request.method == 'PUT':
        quantity = request.form.get('quantity')
        coupons = list()
        for i in range(int(quantity)):
            coupons.append(str(uuid.uuid4())[:18].replace('-', ''))

        return jsonify(list_of_data=coupons)


@promotion.route('/find_coupon', methods=['PUT'])
def find_coupon():
    if request.method == 'PUT':
        code = request.form.get('code')
        data = dict()
        try:
            coupon = Coupon.query.filter_by(code=code, active=True)[0]
        except:
            coupon = None
        code = coupon.code if coupon else None
        if code:
            data = {
                'promotion': code,
                'title': coupon.promotion.title,
                'value': coupon.promotion.discount_value,
                'type': coupon.promotion.discount_type.name
            }
        return  jsonify(**data)


@promotion.route('/apply_promotion', methods=['POST'])
def apply_promotion():
    if request.method == 'POST':
        coupon = Coupon.query.filter_by(code=request.form.get('code'))[0]
        coupon.active = False
        current_user.coupons.extend([coupon])
        current_user.active_discount = True
        db.session.add(coupon)
        db.session.add(current_user)
        db.session.commit()
        return ('', 204)

    