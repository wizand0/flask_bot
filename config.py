import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:


    ##### настройка Flask-Mail #####
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'YOU_MAIL@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME


class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
    #    'mysql+pymysql://root:pass@localhost/flask_app_db'


class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
	#		      'mysql+pymysql://root:pass@localhost/flask_app_db'


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prodbd.db'
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