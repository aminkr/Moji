from flask import Flask

from application.models import db
from application.models.Users import User
from application.models.Payments import Payment
from application.models.Account import Account
from application.blueprints import login_manager


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('application.config.FlaskConfig')

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'

    with app.app_context():
        db.create_all()
        from application.blueprints import paypal
        from application.blueprints import auth
        from application.blueprints import general

        app.register_blueprint(paypal.pay_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(general.gen_bp)

        return app
