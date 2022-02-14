from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, EqualTo, Email
# from wtforms.fields.html5 import EmailField

class SignUp(FlaskForm):
  pass

class LogIn(FlaskForm):
  pass

class AddTodo(FlaskForm):
  pass