import os

from flask import Flask, session
from flask_bootstrap import Bootstrap
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from config import Config
from .models import db, login_manager


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager.init_app(app)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set!!")

bootstrap = Bootstrap(app)


from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

