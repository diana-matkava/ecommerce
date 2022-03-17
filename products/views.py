import os
import sys
from unicodedata import category
from .models import Product
from flask import Blueprint, flash, render_template, redirect, session, url_for, request
from flask_login import current_user
from werkzeug.utils import secure_filename
from ecommerce.extentions import db
from ecommerce.settings import UPLOAD_FOLDER
from ecommerce.utils import allowed_extension
from ecommerce.products.forms import CreateProductForm
from ecommerce.products.models import Product, ProductCategory, Image
from ecommerce.auth.models import Seller, Customer


pr = Blueprint('product', __name__, url_prefix='/product')

@pr.route('/create_product', methods=['GET', 'POST'])
def create_product():
    session.pop('_flashes', None)
    form = CreateProductForm()
    if form.validate_on_submit():
        try:
            product = Product(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                quantity=form.quantity.data,
                owner=str(Seller.query.get(current_user.id))
            )
            product.product_category.extend([ProductCategory.query.get(category) for category in form.category.data])

            images = request.files.getlist('image')
            print(images, file=sys.stdout)
            if images:
                for image in images:
                    if allowed_extension(image.filename):
                        path = os.path.join(UPLOAD_FOLDER, 'img/user_inputs/products/', secure_filename(image.filename))
                        image.save(os.path.join(path))
                        product.image.append([os.path.join('img/user_inputs/customer_avatar/', secure_filename(image.filename))])
                    else:
                        flash('You can appload txt, pdf, png, jpg, jpeg, gif extensions')
            else:
                flash('You have not choose any images')
            
            db.session.add(product)
            db.session.commit()
            flash(f'Product {product} created successfully')
            return redirect(url_for('home'))

        except Exception as _ex:
            flash(f'{_ex}')
            return render_template('products/create_product.html', form=form)
    return render_template('products/create_product.html', form=form)

