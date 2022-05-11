from flask import Flask
from app import app, bc, mongo
from flask import Flask, render_template, request, url_for, request, redirect, abort, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import session, request, render_template, redirect, url_for
from urllib.parse import urlparse, urljoin
import bcrypt
from flask_mail import Mail,Message
from forms import ContactForm
from user.models import User, Anonymous
from user.email_utility import send_registration_email
from user.verification import confirm_token

mail = Mail()
 
app.config["MAIL_SERVER"] = "smtp.mailosaur.net"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = 'alnq3kie@mailosaur.net'
app.config["MAIL_PASSWORD"] = 'KxhspIQecDvJl0kk'
 
mail.init_app(app)

# Create login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"

# LOGIN MANAGER REQUIREMENTS

# Load user from user ID
@login_manager.user_loader
def load_user(userid):
    # Return user object or none
    users = mongo.db.users
    user = users.find_one({'id': userid}, {'_id': 0})
    if user:
        return User.make_from_dict(user)
    return None

# Safe URL
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            # Redirect to index if already authenticated
            return redirect(url_for('/index'))
        # Render login page
        return render_template('login.html', error=request.args.get("error"))
    # Retrieve user from database
    users = mongo.db.users
    user_data = users.find_one({'email': request.form['email']}, {'_id': 0})
    if user_data:
        # Check password hash
        if bc.check_password_hash(user_data['password'], request.form['pass']):
            # Create user object to login (note password hash not stored in session)
            user = User.make_from_dict(user_data)
            login_user(user)

            # Check for next argument (direct user to protected page they wanted)
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)

            # Go to profile page after login
            return redirect(next or url_for('profile'))

    # Redirect to login page on error
    return redirect(url_for('login', error=1))

# Register
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Trim input data
        email = request.form['email'].strip()
        title = request.form['title'].strip()
        reason = request.form['reason'].strip()
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        password = request.form['pass'].strip()

        users = mongo.db.users
        # Check if email address already exists
        existing_user = users.find_one(
            {'email': email}, {'_id': 0})

        if existing_user is None:
            logout_user()
            # Hash password
            hashpass = bc.generate_password_hash(password).decode('utf-8')
            # Create user object (note password hash not stored in session)
            new_user = User(title, reason, first_name, last_name, email)
            # Create dictionary data to save to database
            user_data_to_save = new_user.dict()
            user_data_to_save['password'] = hashpass

            # Insert user record to database
            if users.insert_one(user_data_to_save):
                login_user(new_user)
                send_registration_email(new_user)
                return redirect(url_for('profile'))
            else:
                # Handle database error
                return redirect(url_for('register', error=2))

        # Handle duplicate email
        return redirect(url_for('register', error=1))

    # Return template for registration page if GET request
    return render_template('register.html', error=request.args.get("error"))


# Confirm email
@app.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    logout_user()
    try:
        email = confirm_token(token)
        if email:
            if mongo.db.users.update_one({"email": email}, {"$set": {"verified": True}}):
                return render_template('confirm.html', success=True)
    except:
        return render_template('confirm.html', success=False)
    else:
        return render_template('confirm.html', success=False)


# Verification email
@app.route('/verify', methods=['POST'])
@login_required
def send_verification_email():
    if current_user.verified == False:
        send_registration_email(current_user)
        return "Verification email sent"
    else:
        return "Your email address is already verified"


# Profile
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', title=current_user.title)

# Logout
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index')) 

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()  
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['alnq3kie@mailosaur.net'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
 
      return render_template('contact.html', success=True)
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form) 
