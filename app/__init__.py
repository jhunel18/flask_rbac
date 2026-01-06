from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db, User
from config import Config

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # --- Create tables ---
    with app.app_context():
        db.create_all()

        # Create default admin user if it doesn't exist
        if not User.query.filter_by(role='admin').first():
            admin = User(email="admin@site.com", role="admin")
            admin.set_password("AdminPass123")
            db.session.add(admin)
            db.session.commit()

    from .auth import bp as auth_bp
    from .routes import bp as main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
