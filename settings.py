from environs import Env

env = Env()
env.read_env()

FLASK_APP = env.str('FLASK_APP', default='app.py')
FLASK_ENV = env.str('FLASK_ENV', default='development')
SECRET_KEY = env.str('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = env.str('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOAD_FOLDER = env.str('UPLOAD_FOLDER', 'static/')
ALLOWED_EXTENSIONS = env.str('ALLOWED_EXTENSIONS', {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'})
CURRENCY_API_KEY = env.str('CURRENCY_API_KEY', default=False)

# MAIL_SERVER = 'smtp.googlemail.com'
# MAIL_PORT = 465
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True

# MAIL_USERNAME = env.str['MAIL_USERNAME']
# MAIL_PASSWORD = env.str['MAIL_PASSWORD']