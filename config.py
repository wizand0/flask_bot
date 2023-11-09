import os

"""Flask APP configuration."""
from os import environ, path
from dotenv import load_dotenv


# Specificy a `.env` file containing key/value config values
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOT_TOKEN = environ.get("BOT_TOKEN")
    CHAT_ID = environ.get("CHAT_ID")
    API_FLASK_ARDUINO = environ.get("API_FLASK_ARDUINO")



    ##### настройка Flask-Mail #####
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = MAIL_USERNAME


class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///main.db'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
    #    'mysql+pymysql://root:pass@localhost/flask_app_db'


class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///main.db'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
	#		      'mysql+pymysql://root:pass@localhost/flask_app_db'


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///main.db'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
	#'mysql+pymysql://root:pass@localhost/flask_app_db'


##########
# Features
##########

################
# Flask-Security
################

# URLs
SECURITY_URL_PREFIX = "/admin"
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Включает регистрацию
SECURITY_REGISTERABLE = True
SECURITY_REGISTER_URL = "/register/"
SECURITY_SEND_REGISTER_EMAIL = False

# Включет сброс пароля
SECURITY_RECOVERABLE = True
SECURITY_RESET_URL = "/reset/"
SECURITY_SEND_PASSWORD_RESET_EMAIL = True

# Включает изменение пароля
SECURITY_CHANGEABLE = True
SECURITY_CHANGE_URL = "/change/"
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False