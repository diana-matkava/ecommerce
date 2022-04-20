from flask_admin.contrib.sqla import ModelView
from ecommerce.extentions import admin, db
from ecommerce.products.models import Product, Card, Order, ProductCategory, Currency
from ecommerce.auth.models import Seller, Customer, Type, Category
from ecommerce.checkout.models import Promotion, Coupon
from ecommerce.app import create_app
from ecommerce.extentions import admin




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

app = create_app()
admin.init_app(app)

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