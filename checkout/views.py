import sys
import uuid
import datetime
from ecommerce.checkout.models import Coupon, Promotion
from ecommerce.products.models import Product
from ecommerce.extentions import db
from flask.json import jsonify
from flask import Blueprint, request, render_template, redirect, session, url_for
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
        promotion = Promotion(
            title=request.form.get('title'),
            description=request.form.get('description'),
            discount_type=request.form.get('discount_type'),
            discount_value=int(request.form.get('discount_value')),
            coupon_type=request.form.get('coupon_type'),
            currency=request.form.get('currency'),
            start_day=request.form.get('start_day'),
            end_day=request.form.get('end_day'),
            instant_discount=request.form.get('instant_discount'),
            active=request.form.get('active')
        )

        promotion.products.extend([Product.query.get(product) for product in request.form.get('products')])

        coupons = request.form.get('coupons')
        if coupons:
            for coupon in coupons.splitlines():
                coupon = Coupon(
                    id=coupon,
                    promotion=promotion
                )
                promotion.coupon.extend([coupon])
                coupon.save()
        else:
            code = str(uuid.uuid4())[:18].replace('-', '')
            coupon = Coupon(
                    id=code,
                    promotion=promotion
                )
            promotion.coupon.extend([coupon])
            coupon.save()
        promotion.save()
    return render_template('promotion/create_promotion.html', **data)


@checkout.route('/generate_coupon', methods=['PUT'])
def generate_coupon():
    if request.method == 'PUT':
        quantity = request.form.get('quantity')
        coupons = list()
        for i in range(int(quantity)):
            coupons.append(str(uuid.uuid4())[:18].replace('-', ''))

        return jsonify(list_of_data=coupons)