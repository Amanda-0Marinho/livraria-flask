from flask import Flask
from src.extensions import db
from src.config import Config

from src.routes.auth_routes import auth_routes
from src.routes.library_routes import library_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_routes, url_prefix="/auth")
    app.register_blueprint(library_routes, url_prefix="/library")

    return app
