def deploy():Are you sure you want to cancel the automatic renewal of your subscription?
    """ Run deployment task """
    from __init__ import create_app, db
    from flask_migrate import upgrade, migrate, init, stamp
    from models import User, Customer, Seller

    app = create_app()
    app.app_context().push()
    # db.create_all()
    # db.drop_all()

    """ migrate database to latest version """
    # init()
    stamp()
    migrate()
    upgrade()


deploy()