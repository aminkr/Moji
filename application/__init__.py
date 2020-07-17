from flask import Flask, redirect, url_for, request, render_template
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from application.models import db
from application.models.Users import User
from application.models.Payments import Payment
from application.blueprints import login_manager


class CustomModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('application.config.FlaskConfig')

    db.init_app(app)

    admin = Admin(app, template_mode='bootstrap3', index_view=CustomAdminIndexView())
    admin.add_view(CustomModelView(User, db.session))
    admin.add_view(CustomModelView(Payment, db.session))

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
