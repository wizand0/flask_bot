
from . import app
from flask import render_template, request, redirect, url_for, flash, make_response, session
from flask_login import login_required, login_user,current_user, logout_user
from .models import User, Todo, Sensors, db
from .forms import ContactForm, LoginForm
#from .utils import send_mail









@app.route('/', methods=['GET', 'POST'])
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
        sensor_values = Sensors.query.order_by(Sensors.date_send).all()  # - все записи для отрисовки графика

        # sensors_for_tab = Sensors.query.order_by(Sensors.date_send).limit(3)
        sensors_for_tab = Sensors.query.order_by(Sensors.id.desc()).limit(
            5)  # последине 5 записей в обратном порядке для таблицы
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
                               voltage=voltage, humidity=humidity, sensors_for_tab=sensors_for_tab)  # IMP


# http://127.0.0.1:5000/ard_update?api_key=H20C8OAJ7KXGE3SS&field1=23&field2=44&field3=220&field4=0&field5=0&field6=0 - для тестирования входа API

@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/login/', methods=['post', 'get'])
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
    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))


@app.route("/register", methods=["POST", "GET"])
def register(username=None):
    if request.method == "POST":
        session.pop('_flashes', None)
        if len(request.form['name']) > 4 and len(request.form['username']) > 4 and len(request.form['email']) > 4 \
                and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:

            name = request.form['name'] # Form input Name tag
            email = request.form['email']
            username = request.form['username']
            psw = request.form['psw']
            hash = User.set_password(request.form['psw'])

            new_user = User(name=name, password_hash=hash, email=email, username=username)

            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect("/login/")
            except:
                return "Error creating new task."







            #res = dbase.addUser(request.form['name'], request.form['email'], hash)

        else:
            flash("Неверно заполнены поля", "error")


    #return redirect("/")


@app.route('/ard_update')
def ard_update():
    api_key = request.args.get('api_key')
    temp = request.args.get('field1')
    humidity = request.args.get('field2')
    voltage = request.args.get('field3')

    if api_key == "H20C8OAJ7KXGE3SS":

        new_values = Sensors(temp=temp, humidity=humidity, voltage=voltage)

        try:
            db.session.add(new_values)
            db.session.commit()
            return redirect("/")
        except:
            db.session.rollback()
            print("Ошибка добавления данных сенсоров в БД")
            return "Ошибка добавления данных сенсоров в БД"



    else:

        print("Неправильный API")
        tasks = Todo.query.order_by(Todo.date_created).all()

        sensor_values = Sensors.query.order_by(Sensors.date_send).all()

        return render_template('index.html', tasks=tasks, sensor_values=sensor_values)
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



