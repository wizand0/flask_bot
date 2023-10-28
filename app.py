from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # IMP
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'test@gmail.com'  # введите свой адрес электронной почты здесь
app.config['MAIL_DEFAULT_SENDER'] = 'test@gmail.com'  # и здесь
app.config['MAIL_PASSWORD'] = 'password'  # введите пароль
db = SQLAlchemy(app)
migrate = Migrate(app, db)

mail = Mail(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id






class Sensors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float)
    humidity = db.Column(db.Float)
    voltage = db.Column(db.Integer)
    date_send = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Value %r>' % self.id


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
        sensor_values = Sensors.query.order_by(Sensors.date_send).all()


        date_value = []
        data = []
        voltage = []
        humidity = []
        for row in sensor_values:
            date_value.append(row.date_send)
            data.append(row.temp)
            voltage.append(row.voltage)
            humidity.append(row.humidity)


        #print(sensor_values)
        return render_template('index.html', tasks=tasks, sensor_values=sensor_values, labels2=date_value, data=data,
                               voltage=voltage, humidity=humidity)  # IMP


# http://127.0.0.1:5000/ard_update?api_key=H20C8OAJ7KXGE3SS&field1=23&field2=44&field3=220&field4=0&field5=0&field6=0 - для тестирования входа API


@app.route('/ard_update')
def ard_update():
    api_key = request.args.get('api_key')
    temp = request.args.get('field1')
    humidity = request.args.get('field2')
    voltage = request.args.get('field3')

    if api_key == "H20C8OAJ7KXGE3SS":

        new_values = Sensors(temp=temp, humidity = humidity, voltage = voltage)

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




if __name__ == "__main__":
    app.run(debug=True)

# From Shell
# from app import db,app
# app.app_context().push()
# db.create_all()


