from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth_login"

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    from datetime import datetime

    @app.context_processor
    def inject_now():
        return {'current_year': datetime.now().year}


    app.config.from_object("config.Config")
    app.url_map.strict_slashes = False
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # import modules
        from . import routes, models
        from .models import User, RoleEnum
        db.create_all()
        try:
            admin_user = User.query.filter_by(username="admin").first()
            if not admin_user:
                admin_user = User(username="admin", role=RoleEnum.Admin.value)
                admin_user.set_password("admin123")
                db.session.add(admin_user)
                db.session.commit()
                print("Default admin user created: admin / admin123")
            else:
                admin_user.set_password("admin123")
                admin_user.role = RoleEnum.Admin.value
                db.session.commit()
                print("Admin user updated: admin / admin123")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding admin user: {e}")

    return app

