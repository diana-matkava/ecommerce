import os
import sys
from flask import Flask, send_from_directory, render_template
from ecommerce.admin import BusinessTypeAdminView, CustomerAdminView, ProductAdminView, SellerAdminView
from ecommerce.auth.views import bp, login_manager
from ecommerce.products.views import pr
from ecommerce.checkout.views import checkout, promotion
from ecommerce.extentions import db, migrate, bcrypt, humanize, admin
from ecommerce.auth.models import *
from ecommerce.products.models import *
from ecommerce.checkout.models import *
from flask_admin.contrib.sqla import ModelView

def create_app(test_config=None, config_objects='ecommerce.settings'):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_objects)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     SQLALCHEMY_DATABASE_URI='sqlite:///ecm.sqlite3',
    #     SQLALCHEMY_TRACK_MODIFICATIONS=True
    # )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed inF
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Media
    @app.route('/media/<filename>')
    def media(filename):
        return send_from_directory('/home/diana/Documents/my_projects/ecommerce/ecommerce/media', filename)

    # @app.route('/admin')
    # def admin_index_view():
    #     return render_template('admin/index.html')


    # Registered BluePrints
    app.register_blueprint(bp)
    app.register_blueprint(pr)
    app.register_blueprint(checkout)
    app.register_blueprint(promotion)
    
    # Registered extentions
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    humanize.init_app(app)

    admin.init_app(app,)        # index_view=admin_index_view

    admin.add_view(SellerAdminView(db.session, category='Users', endpoint='admin_sellers'))
    admin.add_view(CustomerAdminView(db.session, category='Users'))
    admin.add_view(BusinessTypeAdminView(db.session, category='Users', name='Business Type'))
    admin.add_view(ModelView(Category, db.session, category='Users', name='Business Category'))

    admin.add_view(ProductAdminView(db.session, category='Products'))
    admin.add_view(ModelView(Order, db.session, category='Products'))
    admin.add_view(ModelView(Card, db.session, category='Products'))
    admin.add_view(ModelView(ProductCategory, db.session, category='Products'))

    admin.add_view(ModelView(Promotion, db.session, category='Checkout', endpoint='promotions'))
    admin.add_view(ModelView(Coupon, db.session, category='Checkout'))
    admin.add_view(ModelView(Currency, db.session, category='Checkout'))

    

    # Register custom command
    # app.cli.add_command(createsuperuser)    

    # @humanize.localeselector
    # def get_locale():
    #     return 'ru_RU'
    return app

app = create_app()
