def deploy():
    """ Run deployment task """
    from ecommerce.app import create_app, db
    from flask_migrate import upgrade, migrate, init, stamp
    from ecommerce.auth.models import Seller, Customer, Type, Category
    import sqlalchemy_utils

    app = create_app()
    app.app_context().push()
    db.create_all()
    db.drop_all()

    """ migrate database to latest version """
    init()
    stamp()
    migrate()
    upgrade()


deploy()