from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    print(f"Loaded JWT_SECRET_KEY: {app.config['JWT_SECRET_KEY']}", flush=True)
    app.logger.info(f"Loaded JWT_SECRET_KEY: {app.config['JWT_SECRET_KEY']}")
    
    db.init_app(app)  
    jwt.init_app(app) 

    from .routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

