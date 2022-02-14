from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, EqualTo, Email

class SignUp(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    email = StringField('email', validators=[Email(), InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Sign Up', render_kw={'class': 'btn waves-effect waves-light white-text'})

class LogIn(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn waves-effect waves-light white-text'})

class AddTodo(FlaskForm):
  text = TextAreaField('Text', validators =[InputRequired()])
  submit = SubmitField('Add', render_kw={'class': 'btn waves-effect waves-light white-text'})