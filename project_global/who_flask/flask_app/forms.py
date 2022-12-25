from flask_wtf import FlaskForm
from wtforms import (
    widgets, RadioField, StringField,
    IntegerField, SelectField, SelectMultipleField,
)
from wtforms.validators import DataRequired


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SurveyForm(FlaskForm):
    age = IntegerField('Возраст')
    city = StringField('В каком городе Вы живёте?')
    occupation = SelectField('Вы сейчас учитесь или работаете?',
                             choices=[('школа', 'Учусь в школе'), ('вуз', 'Учусь в вузе'),
                                      ('работа', 'Работаю'),
                                      ('пенсионер', 'Не работаю, пенсионер'),
                                      ]
                             )
    frequency = RadioField('Насколько часто Вам надо выходить из дома? Отметьте количество раз в неделю.',
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')]
                           )
    times = IntegerField('Сколько часов Вы проводите в общественном транспорте в день? Введите число',
                         )
    means = RadioField('Каким видом транспорта Вы пользуетесь чаще всего?',
                       choices=[('метро', 'Метро'), ('автобус', 'Автобус'), ('трамвай', 'Трамвай'),
                                ('троллейбус', 'Троллейбус'), ('такси', 'Такси'), ('авто', 'Личная машина'),
                                ('мцд', 'МЦД'), ('электричка', 'Электричка'), ('ноги', 'Хожу пешком')],
                       render_kw={'style': 'height: fit-content; list-style: none;'})
    desires = RadioField('Довольны ли Вы тем, как Вы добираетесь на работу/учёбу?',
                         choices=[('Да', 'Да, меня всё устраивает'), ('Нет', 'Нет, мне не нравятся поездки')])

    preferences = RadioField('Какой вид транспорта Вам больше всего нравится?',
                             choices=[('метро', 'Метро'), ('автобус', 'Автобус'), ('трамвай', 'Трамвай'),
                                      ('троллейбус', 'Троллейбус'), ('такси', 'Такси'),
                                      ('авто', 'Личная машина'), ('мцд', 'МЦД'),
                                      ('электричка', 'Электричка'), ('ноги', 'Хожу пешком')
                                      ], render_kw={'style': 'height: fit-content; list-style: none;'}
                             )
