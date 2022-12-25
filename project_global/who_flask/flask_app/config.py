import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'survey.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = "run_flask_app.py"
