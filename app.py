import os
import json
from flask import Flask, Markup, send_from_directory, render_template
from .admin import BusinessTypeAdminView, CustomerAdminView, ProductAdminView, SellerAdminView
from .auth.views import bp, login_manager
from .products.views import pr
from .checkout.views import checkout, promotion
from .extentions import db, migrate, bcrypt, humanize, admin
from .auth.models import *
from .products.models import *
from .checkout.models import *
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.jinja_env.filters['json'] = lambda v: Markup(json.dumps(v))

from email.policy import default
from environs import Env

env = Env()
env.read_env()



def create_app(test_config=None, config_objects='.settings.py'):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object(config_objects)
    app.config.from_mapping(
        FLASK_APP = env.str('FLASK_APP', default='app.py'),
        FLASK_ENV = env.str('FLASK_ENV', default='development'),
        SECRET_KEY = env.str('SECRET_KEY', default='surepHardSecretKye'),
        SQLALCHEMY_DATABASE_URI = env.str('SQLALCHEMY_DATABASE_URI', default='sqlite:///ecm.sqlite3'),
        SQLALCHEMY_TRACK_MODIFICATIONS = True,
        UPLOAD_FOLDER = env.str('UPLOAD_FOLDER', 'static/'),
        ALLOWED_EXTENSIONS = env.list('ALLOWED_EXTENSIONS', default=['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']),
        CURRENCY_API_KEY = env.str('CURRENCY_API_KEY', default='True'),
    )

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
        return send_from_directory('/home/diana/Documents/my_projects///media', filename)

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
