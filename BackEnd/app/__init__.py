from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler
from config import config
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
scheduler = APScheduler()

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key_here')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    if not scheduler.running:
        scheduler.init_app(app)
        scheduler.start()

    from .routes.auth import auth_bp
    from .routes.books import books_bp
    from .routes.cart import cart_bp
    from .routes.orders import orders_bp
    from .routes.users import users_bp
    from .routes.admin import admin_bp
    from .routes.feedback import feedback_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(feedback_bp, url_prefix='/feedback')

    return app
