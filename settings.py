from environs import Env

env = Env()
env.read_env()

FLASK_APP = env.str('FLASK_APP', default='app.py')
FLASK_ENV = env.str('FLASK_ENV', default='development')
SECRET_KEY = env.str('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = env.str('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOAD_FOLDER_SELLER = env.str('UPLOAD_FOLDER_SELLER', 'media/seller_logo/')
UPLOAD_FOLDER_CUSTOMER = env.str('UPLOAD_FOLDER_CUSTOMER', 'media/customer_image/')
ALLOWED_EXTENSIONS = env.str('ALLOWED_EXTENSIONS', {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'})