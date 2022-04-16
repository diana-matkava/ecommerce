from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_humanize import Humanize

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)

db=SQLAlchemy(metadata=metadata)

migrate = Migrate()
bcrypt = Bcrypt()
bootstrap = Bootstrap()
humanize = Humanize()