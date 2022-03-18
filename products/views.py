import datetime
import os
import sys
from unicodedata import category
from .models import Product
from flask import Blueprint, flash, render_template, redirect, session, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from ecommerce.extentions import db
from ecommerce.settings import UPLOAD_FOLDER
from ecommerce.utils import allowed_extension
from ecommerce.products.forms import CreateProductForm
from ecommerce.products.models import Product, ProductCategory, Image
from ecommerce.auth.models import Seller, Customer


pr = Blueprint('', __name__, url_prefix='/')


@pr.route('/')
def home():
    data = {
        'products': Product.query.all(),
        'time': datetime.datetime.now()
    }
   
    return render_template('products/home-page.html', **data)


@pr.route('/<id>', methods=['GET', 'POST'])
def product_page(id):
    product = Product.query.get(id)
    return render_template('products/product-page.html', product=product)


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
                owner=current_user.email
            )
            product.product_category.extend([ProductCategory.query.get(category) for category in form.category.data])

            images = request.files.getlist('image')
            print(images, file=sys.stdout)
            if images:
                for image in images:
                    if allowed_extension(image.filename):
                        path = os.path.join(UPLOAD_FOLDER, 'img/user_inputs/products/', secure_filename(image.filename))
                        image.save(os.path.join(path))
                        product_image = Image(path=os.path.join('img/user_inputs/products/', secure_filename(image.filename)))
                        db.session.add(product_image)
                        product.images.extend([product_image])
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
            db.session.rollback()
            return render_template('products/create_product.html', form=form)
        finally:
            db.session.close()
    return render_template('products/create_product.html', form=form)

@login_required
@pr.route('/edit_product/<id>', methods=['GET', 'POST'])
def edit_product(id):
    session.pop('_flashes', None)
    form = CreateProductForm()

    return render_template('products/edit_product.html', form=form)