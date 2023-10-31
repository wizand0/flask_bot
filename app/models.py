from app import db, login_manager
from datetime import datetime
from flask_login import (LoginManager, UserMixin, login_required,
                         login_user, current_user, logout_user)
from flask_security import RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    # Нужен для security!
    active = db.Column(db.Boolean())
    # Для получения доступа к связанным объектам
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

        # Flask - Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # Flask-Security
    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def set_password(self, password):
        password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

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
