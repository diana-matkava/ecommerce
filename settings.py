from environs import Env

env = Env()
env.read_env()

FLASK_APP = env.str('FLASK_APP', default='app.py')
FLASK_ENV = env.str('FLASK_ENV', default='development')
SECRET_KEY = env.str('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = env.str('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = True