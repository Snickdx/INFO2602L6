import json
from flask_login import LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db, User, Todo
from forms import SignUp, LogIn, AddTodo

''' Begin boilerplate code '''

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

''' End Flask Login Functions '''

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  login_manager.init_app(app)
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()
db.create_all(app=app)
''' End Boilerplate Code '''

@app.route('/', methods=['GET'])
def index():
  form = LogIn()
  return render_template('login.html', form=form)

#user submits the login form
@app.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): # respond to form submission
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): # check credentials
        flash('Logged in successfully.') # send message to next page
        login_user(user) # login the user
        return redirect(url_for('todos')) # redirect to main page if login successful
  flash('Invalid credentials')
  return redirect(url_for('index'))

@app.route('/users', methods=['GET'])
def get_todos():
  users = User.query.all()
  results = []
  return json.dumps([ user.toDict() for user in users ])

@app.route('/signup', methods=['GET'])
def signup():
  signup = SignUp() # create form object
  return render_template('signup.html', form=signup) # pass form object to template

@app.route('/signup', methods=['POST'])
def signupAction():
  form = SignUp() # create form object
  if form.validate_on_submit():
    data = request.form # get data from form submission
    newuser = User(username=data['username'], email=data['email']) # create user object
    newuser.set_password(data['password']) # set password
    db.session.add(newuser) # save new user
    db.session.commit()
    flash('Account Created!')# send message
    return redirect(url_for('index'))# redirect to login page
  flash('Error invalid input!')
  return redirect(url_for('signup')) 

@app.route('/todos', methods=['GET'])
@login_required
def todos():
  todos = Todo.query.filter_by(userid=current_user.id).all()
  if todos is None:
      todos = [] # if user has no todos pass an empty list
  form = AddTodo()
  return render_template('todo.html', form=form, todos=todos)

@app.route('/todos', methods=['POST'])
@login_required
def todosAction():
  form = AddTodo()
  if form.validate_on_submit():
    data = request.form # get request data
    todo = Todo(text=data['text'], done=False, userid=current_user.id) # create todo object
    db.session.add(todo) # save todo object
    db.session.commit()
    flash('Todo Created!') # send message
    return redirect(url_for('todos')) # redirect
  flash('Invalid data!')
  return redirect(url_for('todos')) # redirect

app.run(host='0.0.0.0', port=8080, debug=True)