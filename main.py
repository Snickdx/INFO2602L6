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

@app.route('/')
def index():
  return render_template('login.html')

@app.route('/todos', methods=['GET'])
def todos():
  return render_template('todo.html')

@app.route('/users', methods=['GET'])
def get_todos():
  users = User.query.all()
  results = []
  for user in users:
    rec = user.toDict() # convert user object to dictionary record
    rec['num_todos'] = user.getNumTodos() # add num todos to dictionary record
    rec['num_done'] = user.getDoneTodos() # add num done todos to dictionary record
    results.append(rec)
  return json.dumps(results)

app.run(host='0.0.0.0', port=8080)