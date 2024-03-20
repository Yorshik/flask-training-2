import fnmatch
import json
import os

from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.debug = True


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
    for member_dct in members['crew_members']:
        member_dct['specialities'] = ', '.join(sorted(member_dct['specialities']))
    return render_template('member.html', crew_members=members)


@app.route('/table_param/<sex>/<int:age>')
def table_param(sex, age):
    return render_template('table_param.html', sex=sex, age=age)


@app.route('/astronaut_selection', methods=['POST', "GET"])
def astronaut_selection():
    if request.method == 'GET':
        return f'''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
            crossorigin="anonymous">
            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
            <title>Пример формы</title>
          </head>
          <body>
            <h1 class="mytext">Анкета претендента</h1>
            <h2 class="mytext">на участие в миссии</h2>
            <div>
              <form class="login_form" method="post">
                <input type="text" class="form-control" id="surname" aria-describedby="format" placeholder="Введите фамилию" name="surname">
                <input type="text" class="form-control" id="name" placeholder="Введите имя" name="name">
                <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                <div class="form-group">
                  <label for="classSelect">Какое у вас образование?</label>
                  <select class="form-control" id="classSelect" name="education">
                    <option>Начальное</option>
                    <option>Среднее общее</option>
                    <option>Среднее полное</option>
                    <option>Среднее Профессиональное</option>
                    <option>Высшее</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="form-speciality">Какие у Вас есть профессии?</label>
                  <div class="form-check">
                    <input type="checkbox" class="form-speciality-input" id="1" name="check1">
                    <label class="form-speciality-label" for="1" name="label1">Инженер-исследователь</label>
                  </div>
                  <div class="form-check">
                    <input type="checkbox" class="form-speciality-input" id="2" name="check2">
                    <label class="form-speciality-label" for="2" name="label2">Инженер-строитель</label>
                  </div>
                  <div class="form-check">
                    <input type="checkbox" class="form-speciality-input" id="3" name="check3">
                    <label class="form-speciality-label" for="3" name="label3">Пилот</label>
                  </div>
                  <div class="form-check">
                    <input type="checkbox" class="form-speciality-input" id="4" name="check4">
                    <label class="form-speciality-label" for="4" name="label4">Метеоролог</label>
                  </div>
                  <div class="form-check">
                    <input type="checkbox" class="form-speciality-input" id="5" name="check5">
                    <label class="form-speciality-label" for="5" name="label5">Инженер по жизнеобеспечению</label>
                  </div>
                  <div class="form-check">
                    <input type="checkbox" class="form-speciality-input" id="6" name="check6">
                    <label class="form-speciality-label" for="6" name="label6">Инженер по радиационной защите</label>
                  </div>
                  <div class="form-check">
                    <input type="checkbox" class="form-speciality-input" id="7" name="check7">
                    <label class="form-speciality-label" for="7" name="label7">Врач</label>
                  </div>
                  <div class="form-check">
                    <input type="checkbox" class="form-speciality-input" id="8" name="check8">
                    <label class="form-speciality-label" for="8" name="label8">Экзобиолог</label>
                  </div>
                </div>
                <div class="form-group">
                  <label for="form-check">Укажите пол</label>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                    <label class="form-check-label" for="male">
                      Мужской
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                    <label class="form-check-label" for="female">
                      Женский
                    </label>
                  </div>
                  </div>
                  <div class="form-group">
                    <label for="about">Почему Вы хотите принять участие в миссии</label>
                    <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                  </div>
                  <div class="form-group">
                    <label for="photo">Приложите фотографию</label>
                    <input type="file" class="form-control-file" id="photo" name="file">
                  </div>
                  <div class="form-group form-check">
                    <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                    <label class="form-check-label" for="acceptRules">Готовы остаться на Марсе?</label>
                  </div>
                  <button type="submit" class="btn btn-primary">Отправить</button>
                </form>
              </div>
            </body>
          </html>'''
    elif request.method == 'POST':
        global dct
        dct['title'] = 'Анкета'
        try:
            dct['surname'] = request.form['surname']
            dct['name'] = request.form['name']
            dct['education'] = request.form['education']
            dct['sex'] = request.form['sex']
            dct['motivation'] = request.form['about']
            dct['accept'] = request.form['accept']
        except BaseException as e:
            print(e)
        lst = []
        profs = {
            1: 'Инженер-исследователь',
            2: 'Инженер-строитель',
            3: 'Пилот',
            4: 'Метеоролог',
            5: 'Инженер по жизнеобеспечению',
            6: 'Инженер по радиационной защите',
            7: 'Врач',
            8: 'Экзобиолог'
        }
        for i in range(1, 9):
            if request.form.get(f'check{i}'):
                lst.append(profs[i])
        dct['profession'] = ', '.join(lst)
        return redirect(url_for('answer'))


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    return render_template('auto_answer.html', dct=dct)


@app.route('/gallery', methods=["GET", 'POST'])
def gallery():
    if request.method == 'POST':
        lst = []
        for name in os.listdir('static/img'):
            if fnmatch.fnmatch(name, 'mars*.png'):
                lst.append(name)
        lst.sort()
        last = lst[-1]
        new = last[:4] + str(int(last[4]) + 1) + last[5:]
        file = request.files['add_file']
        print(file.save(f'static/img/{new}'))
    matches = 0
    for name in os.listdir('static/img'):
        if fnmatch.fnmatch(name, 'mars*.png'):
            matches += 1
    return render_template('gallery.html', n=matches)


dct = {}
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
