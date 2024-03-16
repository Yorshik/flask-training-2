import json

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


class LoginForm(FlaskForm):
    captain_id = StringField('Captain`s id', validators=[DataRequired()])
    captain_pass = PasswordField('Captain`s password', validators=[DataRequired()])
    astronaut_id = StringField('Astronaut`s id', validators=[DataRequired()])
    astronaut_pass = PasswordField('Astronaut`s password', validators=[DataRequired()])
    submit = SubmitField('Доступ')


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def training(prof):
    return render_template('trainig.html', prof=prof.lower())


@app.route('/list_prof/<lst>')
def list_prof(lst):
    professions = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач',
                   'инженер по терраформированию', 'климатолог',
                   'специалист по радиационной защите', 'астрогеолог', 'гляциолог',
                   'инженер жизнеобеспечения', 'метеоролог', 'оператор марсохода', 'киберинженер',
                   'штурман', 'пилот дронов']
    return render_template('list_prof.html', professions=professions, list=lst)


@app.route('/distribution')
def distribution():
    astronauts = {
        'astronauts.json': [
            'Ридли Скотт',
            "Энди Уир",
            "Марк Уотни",
            "Венката Капур",
            "Тедди Сандерс",
            "Шон Бин"
        ]
    }
    return render_template('distribution.html', astronauts=astronauts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return 'Доступ разрешен'
    return render_template('login.html', form=form)


@app.route('/member')
def member():
    with open('templates/astronauts.json', encoding='UTF-8') as js:
        members = json.load(js)
    return render_template('member.html', crew_members=members)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
