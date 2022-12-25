import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_app.config import Config

SECRET_KEY = os.urandom(32)


def create_app():
    app_b = Flask(__name__)
    Bootstrap(app_b)

    return app_b


app = create_app()
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['SECRET_KEY'] = SECRET_KEY

from flask_app import routes, models
