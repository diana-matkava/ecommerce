from ast import Pass
import os.path
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ecommerce.auth.models import Seller, Customer
from app import create_app


app = create_app()

def createsuperuser():
    with app.app_context():
        from ecommerce.auth.views import create_superuser
        x = 1
        while x:
            email =  input('Email: ')
            seller = Seller.query.filter_by(email=email)
            customer = Customer.query.filter_by(email=email)
            if '@' not in email:
                print('Input valid email')
            else:
                password = input('Password: ')
                while len(password) < 7:
                    print('Password too short, please provide at least 8 characters')
                    password = input('Password: ')

                c_password = input('Confirm password: ')
                if password != c_password:
                    print('Password mismatch')
                else:
                    print('SuperUser was created')
                    x = 0




# def createsuperuser():
    

if __name__ == "__main__":
    createsuperuser()
