from flask_admin.contrib.sqla import ModelView
from ecommerce.extentions import admin, db
from ecommerce.products.models import Product
from ecommerce.auth.models import Seller, Customer, Type
from ecommerce.checkout.models import Promotion


class CustomerAdminView(ModelView):
    can_view_details = True
    column_list = ['id', 'email', 'username', 'role', 'card_id', 'currency', 'active_discount']
    
    def __init__(self, session, **kwargs):
        super(CustomerAdminView, self).__init__(Customer, session, **kwargs)


class SellerAdminView(ModelView):
    can_view_details = True
    column_exclude_list = ('password')

    def __init__(self, session, **kwargs):
        super(SellerAdminView, self).__init__(Seller, session, **kwargs)


class ProductAdminView(ModelView):
    can_view_details = True
    column_exclude_list = ('description')

    def __init__(self, session, **kwargs):
        super(ProductAdminView, self).__init__(Product, session, **kwargs)


class BusinessTypeAdminView(ModelView):
    can_view_details = True
    # column_exclude_list = ('busines_type')

    def __init__(self, session, **kwargs):
        super(BusinessTypeAdminView, self).__init__(Type, session, **kwargs)


class PromotionAdminView(ModelView):
    can_view_details = True
    # column_exclude_list = ('busines_type')

    def __init__(self, session, **kwargs):
        super(PromotionAdminView, self).__init__(Promotion, session, **kwargs)
        self.name = 'sdsdsdsd'

