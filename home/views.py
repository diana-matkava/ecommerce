import datetime
from flask import Blueprint, render_template
from ..extentions import db
from ..products.models import Product, ProductCategory


main = Blueprint('main', __name__, url_prefix='/')


@main.route('/', methods=['GET', 'POST', 'PUT'])
@main.route('/<id>', methods=['GET', 'POST', 'PUT'])
def home(id=None):
    data = {
        'ad_products':  Product.query.all()[::4],
        'products': Product.query.all() if not id \
            else db.session.query(Product).filter(
                Product.product_category.any(ProductCategory.id.in_([id]))),
        'time': datetime.datetime.now(),
        'categories': ProductCategory.query.all(),
    }
    # if request.method == 'POST':
        # search = request.form['search']
        # data['products'] = Product.query.filter(Product.name.contains(search)).all()
    return render_template('home/home.html', **data)