from locale import currency
import sys
import uuid
import datetime
from xmlrpc.client import boolean
from ecommerce.checkout.models import Coupon, Currency, Promotion, DiscountType, CouponType
from ecommerce.products.models import Product
from ecommerce.extentions import db
from flask.json import jsonify
from flask import Blueprint, request, render_template, redirect, session, url_for, flash
from flask_login import current_user, login_required
from ecommerce.checkout.forms import PromotionForm


checkout = Blueprint('checkout', __name__, url_prefix='/checkout')

@checkout.route('/marketing_tools', methods=['GET'])
def marketing_tools():
    return render_template('promotion/marketing_tools.html')


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