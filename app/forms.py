from flask_wtf import FlaskForm
from wtforms import Form, ValidationError, PasswordField
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email, InputRequired


class ContactForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    # email = StringField("Email: ", Email())
    email = StringField("Email: ", validators=[Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField()


class RegistrationForm(FlaskForm):
    name = StringField('name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    email = EmailField('Email address', validators=[Email()])
    password = PasswordField('Password', validators=[InputRequired()])
