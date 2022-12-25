from flask_app import app
from flask import render_template, redirect
from flask_app.config import Config
from sqlalchemy import func
from flask_app.forms import SurveyForm
from flask_app import db
from flask_app.models import RespondentData, Responses


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/anketa', methods=['POST', 'GET'])
def opros():
    form = SurveyForm()
    if form.validate_on_submit():
        new_anketa1 = RespondentData(
            age=form.age.data,
            occupation=form.occupation.data,
            frequency=form.frequency.data,

        )
        db.session.add(new_anketa1)
        db.session.commit()
        db.session.refresh(new_anketa1)
        new_anketa2 = Responses(
            res_id=new_anketa1.id,
            times=form.times.data,
            means1=form.means.data,
            desires=form.desires.data,
            preference=form.preferences.data
        )
        db.session.add(new_anketa2)
        db.session.commit()
        return redirect('/thanks')
    return render_template('opros2.html', form=form)


@app.route('/thanks')
def thanks():
    return render_template('finished.html')


@app.route('/result')
def result():
    da_data = {}
    age_stats = db.session.query(
            func.avg(RespondentData.age),
            func.min(RespondentData.age),
            func.max(RespondentData.age)).one()
    da_data['age_mean'] = age_stats[0]
    da_data['age_min'] = age_stats[1]
    da_data['age_max'] = age_stats[2]
    da_data['freq_max'] = db.session.query((func.max(RespondentData.frequency))).one()[0]
    da_data['freq_min'] = db.session.query((func.min(RespondentData.frequency))).one()[0]
    da_data['school'] = db.session.query(RespondentData).filter(RespondentData.occupation == 'школа').count()
    da_data['student'] = db.session.query(RespondentData).filter(RespondentData.occupation == 'вуз').count()
    da_data['work'] = db.session.query(RespondentData).filter(RespondentData.occupation == 'работа').count()
    da_data['pension'] = db.session.query(RespondentData).filter(RespondentData.occupation == 'пенсионер').count()
    da_data['time'] = db.session.query((func.avg(Responses.times))).one()[0]
    means_list = db.session.query(func.count(Responses.means1), Responses.means1).\
        group_by(Responses.means1).order_by(func.count(Responses.means1).desc()).all()
    da_data['means_num'] = means_list[0][0]
    da_data['means_name'] = means_list[0][1]
    da_data['happy'] = db.session.query(Responses).filter(Responses.desires == 'Да').count()
    popular_list = db.session.query(Responses.preference, func.count(Responses.preference)).\
        group_by(Responses.preference).order_by(func.count(Responses.preference).desc()).all()
    da_data['popular'] = popular_list[0][0]
    da_data['persons'] = popular_list[0][1]
    return render_template("tmp_opros_reesult.html", da_data=da_data)
