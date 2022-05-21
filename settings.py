from email.policy import default
from environs import Env

env = Env()
env.read_env()

FLASK_APP = env.str('FLASK_APP', default='app.py')
FLASK_ENV = env.str('FLASK_ENV', default='development')
SECRET_KEY = env.str('SECRET_KEY', default='surepHardSecretKye')
SQLALCHEMY_DATABASE_URI = env.str('SQLALCHEMY_DATABASE_URI', default='sqlite:///ecm.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOAD_FOLDER = env.str('UPLOAD_FOLDER', 'static/')
ALLOWED_EXTENSIONS = env.list('ALLOWED_EXTENSIONS', default=['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
CURRENCY_API_KEY = env.str('CURRENCY_API_KEY', default='True')

# MAIL_SERVER = 'smtp.googlemail.com'
# MAIL_PORT = 465
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True

# MAIL_USERNAME = env.str['MAIL_USERNAME']
# MAIL_PASSWORD = env.str['MAIL_PASSWORD']