import os
from flask import Flask, render_template, request, redirect
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from .forms import ContactForm, LoginForm
from flask_bootstrap import Bootstrap5



# создание экземпляра приложения
app = Flask(__name__)
bootstrap = Bootstrap5(app)
# app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')
#app.config.from_object('config.DevelopementConfig')
app.config.from_object('config.ProductionConfig')

# инициализирует расширения
db = SQLAlchemy(app)
admin = Admin(template_mode="bootstrap4")
mail = Mail(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'



## Регистрация путей Blueprint
#from .admin.routes import admin_bp
#app.register_blueprint(admin_bp, url_prefix="/admin")

# import views
from . import views
# from . import forum_views
# from . import admin_views


