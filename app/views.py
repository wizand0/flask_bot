import requests
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, current_user, logout_user

from . import app
from app import db, login_manager
from datetime import datetime, timedelta

import config
from config import BaseConfig


from .forms import LoginForm, RegistrationForm
#from . import db
from .models import User, Todo, Sensors, VoltageOff
from werkzeug.security import generate_password_hash, check_password_hash

# from .utils import send_mail

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        task_content = request.form['content']  # Form input Name tag
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "Error creating new task."

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        #sensor_values = Sensors.query.order_by(Sensors.date_send).all()  # - все записи для отрисовки графика; тип List

        sensor_values = Sensors.query.order_by(Sensors.date_send).all()[-120::5] # Если в sensor_values получается тип
        # Query то с помощью срезов остается List. В шаблоне индекс в части: {%if sensor_values|length < 1 %} нужен
        # именно List - у Query нет функции len()

        #sensor_values = Sensors.query.order_by(Sensors.id.desc()).limit(50) # - последние 50 записей для графика

        # sensors_for_tab = Sensors.query.order_by(Sensors.date_send).limit(3)
        sensors_for_tab = Sensors.query.order_by(Sensors.id.desc()).limit(
25)  # последине 5 записей в обратном порядке для таблицы

        voltage_off = VoltageOff.query.order_by(VoltageOff.date_send).all()[-15:] #Последние 15 отключений электричества

        # sensors_for_tab = sensors_for_tab[::-1]




        date_value = []
        data = []
        voltage = []
        humidity = []
        for row in sensor_values:
            date_value.append(row.date_send)
            data.append(row.temp)
            voltage.append(row.voltage)
            humidity.append(row.humidity)

        # print(sensor_values)
        return render_template('index.html', tasks=tasks, sensor_values=sensor_values, labels2=date_value, data=data,
                               voltage=voltage, humidity=humidity, sensors_for_tab=sensors_for_tab,
                               voltage_off=voltage_off)  # IMP

# http://127.0.0.1:5000/ard_update?api_key=H20C8OAJ7KXGE3SS&field1=23&field2=44&field3=220&field4=0&field5=0&field6=0
# - для тестирования входа API

@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/login', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('admin'))

        flash("Invalid username/password", 'error')
        return redirect(url_for('login'))
    #return render_template('loging.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))
# register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        username = form.username.data
        user = User(name=name, username=username, email=email)
        user.password_hash = generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        flash("Registration was successfull, please login")
        return redirect(url_for('login'))
    else:
        print("Error form")
    return render_template('registration.html', form=form)


#API для добавление в БД данных сенсоров на arduino
@app.route('/ard_update',methods = ['POST', 'GET'])
def ard_update():
    key = request.args.get('key')
    temp = float(request.args.get('field1'))
    humidity = int(request.args.get('field2'))
    voltage = int(request.args.get('field3'))


    if key == BaseConfig.API_FLASK_ARDUINO:
        TELEGRAM_URL = "https://api.telegram.org/bot"
        part_url_for_1 = "/sendMessage?chat_id="
        chat_id = BaseConfig.CHAT_ID
        part_url_for_2 = "&text="
        text = "Внимание: ОТКЛЮЧЕНИЕ ЭЛЕКТРИЧЕСТВА. ДАТА: "
        BOT_TOKEN = BaseConfig.BOT_TOKEN
        now = datetime.now() + timedelta(hours=3)
        now_str = str(now)

        #request_telegram = TELEGRAM_URL + BOT_TOKEN + part_url_for_1 + chat_id + part_url_for_2 + text + now_str

        new_values = Sensors(temp=temp, humidity=humidity, voltage=voltage, date_send=now)
        try:
            db.session.add(new_values)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления данных сенсоров в БД")
            return "Ошибка добавления данных сенсоров в БД"

        obj1, obj2 = Sensors.query.order_by(Sensors.id.desc()).limit(2)

#        print(obj2.date_send)
#        print(obj1.date_send)

        delta = obj1.date_send - obj2.date_send
        delta1 = int(delta.total_seconds() / 60)

#        print(delta)
#        print(delta1)

        if delta1 > 15:
            text = "Внимание: Большое время между отправкой данных. Время: "
            request_telegram = TELEGRAM_URL + BOT_TOKEN + part_url_for_1 + chat_id + part_url_for_2 + text + now_str
            # return redirect(request_telegram)
            resp = requests.get(request_telegram)
            api_answer = resp.json()
            api_answer_status = api_answer["ok"]
#            print(type(api_answer))
#            print(api_answer[0])

            return render_template("ok.html", api_answer_status=api_answer_status)


        if voltage < 15:
            text = "Внимание: отключение электричества. Время: "
            request_telegram = TELEGRAM_URL + BOT_TOKEN + part_url_for_1 + chat_id + part_url_for_2 + text + now_str
            voltage_off = VoltageOff(voltage=voltage, date_send=now)
            try:
                db.session.add(voltage_off)
                db.session.commit()
            except:
                db.session.rollback()
                print("Ошибка добавления данных сенсоров в БД")

            #return redirect(request_telegram)
            resp = requests.get(request_telegram)
            api_answer = resp.json()
            api_answer_status = api_answer["ok"]
#            print(resp)
#            print("______________________________")

#            print(type(api_answer))
#            print(api_answer_status)

            return render_template("ok.html", api_answer_status=api_answer_status)
        else:
            return redirect("/")
        #return redirect(request_telegram)
    else:
        print("Неправильный API")
        # tasks = Todo.query.order_by(Todo.date_created).all()
        # sensor_values = Sensors.query.order_by(Sensors.date_send).all()
        #https://api.telegram.org/bot6164575119:AAEYx-IP2hSZgf2IpsHLztULW1I55jyhP2Q/sendMessage?chat_id=299472815&text=тдтолидлилил
        return redirect("/")
        # IMP

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)  # IMP
    # When you use Todo.query, it creates a query object for the Todo model,
    # which allows you to perform queries on the todos table.

    try:
        db.session.delete(task_to_delete)
        # db is an instance of SQLAlchemy, which is used to manage the connection and interaction with
        # the database. However, to perform queries on the Todo model,
        # we need to use the query method of the Todo model.
        db.session.commit()
        return redirect("/")
    except:
        return "Error Deleting Task"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Error Updating Task"

    else:
        return render_template('update.html', task=task)
