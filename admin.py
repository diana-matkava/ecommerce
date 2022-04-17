from flask_admin.contrib.sqla import ModelView
from ecommerce.extentions import admin, db
from ecommerce.products.models import Product
from ecommerce.auth.models import Seller, Customer


class CustomerAdminView(ModelView):
    # Disable model creation
    can_create = False

    # Override displayed fields
    column_list = ('username', 'email')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(CustomerAdminView, self).__init__(Customer, session, **kwargs)