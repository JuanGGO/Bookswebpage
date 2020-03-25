import os

from flask import Flask, session
from flask_bootstrap import Bootstrap
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set!!")

bootstrap = Bootstrap(app)
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)
