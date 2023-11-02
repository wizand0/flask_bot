from app import db, login_manager
from datetime import datetime
from flask_login import (LoginManager, UserMixin, login_required,
                         login_user, current_user, logout_user)
from flask_security import RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

        # Flask - Login
    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def set_password(self, password_hash):
        self.password_hash = generate_password_hash(password_hash)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Отвечает за сессию пользователей. Запрещает доступ к роутам, перед которыми указано @login_required
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


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


class VoltageOff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voltage = db.Column(db.Integer)
    date_send = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Value %r>' % self.id