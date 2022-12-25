from flask_app import db
from flask_app import app
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship


class RespondentData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(200))
    frequency = db.Column(db.Integer)


class Responses(db.Model):
    response_id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer, db.ForeignKey('respondent_data.id'))
    times = db.Column(db.Integer)
    means1 = db.Column(db.String(200))
    desires = db.Column(db.String(200))
    preference = db.Column(db.String(200))

    def __repr__(self):
        return f'<Anketa from "{self.username}"/"{self.email}">'


with app.app_context():
    db.create_all()
