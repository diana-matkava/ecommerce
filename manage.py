import os.path
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from .auth.models import Seller, Customer
from app import create_app
from extentions import db
from flask import session
from .auth.views import create_superuser, load_user

app = create_app()
app.app_context().push()

def createsuperuser():
    with app.app_context():
        from .auth.views import create_superuser
        x = 1
        while x:
            seller = 1
            customer = 0
            while seller + customer > 0:
                email =  input('Email: ')
                seller = Seller.query.filter_by(email=email).count()
                customer = Customer.query.filter_by(email=email).count()
                if '@' not in email:
                    print('Input valid email')
                elif seller + customer > 0:
                    print('This email already taken')
                else:
                    password, c_password = 1, 0
                    while password != c_password:
                        password = input('Password: ')
                        while len(password) < 7:
                            print('Password too short, please provide at least 8 characters')
                            password = input('Password: ')
                        c_password = input('Confirm password: ')
                        if password != c_password:
                            print('Password mismatch')
                        else:
                            with app.test_request_context():
                                superuser = Seller(email=email, password=password, role=2)
                                db.session.add(superuser)
                                session['role'] = 2
                                db.session.commit()
                                load_user(superuser.id)
                            print('SuperUser was created')
                        x = 0


if __name__ == "__main__":
    createsuperuser()
