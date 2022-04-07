import os                 # os is used to get environment variables IP & PORT
from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
client = pymongo.MongoClient("mongodb://TeamNine:W5QSpI81YBBHrgas@cluster0-shard-00-00.ljtel.mongodb.net:27017,cluster0-shard-00-01.ljtel.mongodb.net:27017,cluster0-shard-00-02.ljtel.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-vp85gf-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.user_login_system

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# Routes
from user import routes

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.