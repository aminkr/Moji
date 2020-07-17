from flask import Flask

from application.models import db
from application.models.Users import User
from application.models.Payments import Payment
from application.blueprints import login_manager
from flask_bcrypt import Bcrypt

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('application.config.FlaskConfig')


db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'

bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()

    admin_hash = bcrypt.generate_password_hash('Admin,.123')
    admin = User(username='admin', password=admin_hash, email='admin@admin.com', is_admin=True)

    db.session.add(admin)
    db.session.commit()