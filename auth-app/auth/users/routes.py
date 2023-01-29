from flask import render_template, url_for, flash, redirect, request, Blueprint
from auth import bcrypt, login_manager, UserMixin, login_required, login_user, logout_user, current_user
from auth.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from auth.users.db_query import register_user, log_in_user, validate_username, load_user_query
import sqlite3

users = Blueprint('users', __name__)

class User(UserMixin):
    def __init__(self, id, username, password):
        unicode=str
        self.id = unicode(id)
        self.username = username
        self.password = password
        self.authenticated = False
    def is_active(self):
        return self.is_active()
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return self.authenticated
    def is_active(self):
        return True
    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    msg,lu = load_user_query(user_id)
    if lu is None:
        return None
    else:
        return User(int(lu['user_id']), lu['username'], lu['password'])


@users.route("/")
def home():
    return render_template('index.html', title='Home')

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if request.method == 'POST':        
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            username = form.username.data
            email = form.email.data
            name = form.name.data
            
            data = {'username':username, 
                        'email':email, 
                        'password':hashed_password,
                        'name': name}
            
            msg = register_user(data)
            if msg['success_msg'] == "Table entry inserted successfully.":
                flash('Your account has been created! You are now able to log in', 'success')
                return redirect(url_for('users.login'))
            elif msg['error_msg'] == "Error in insert operation.":
                flash('There has been an error in operation.', 'danger')

    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = LoginForm()
    if form.validate_on_submit():
        msg,is_username_available,user = validate_username(form.username.data)
        Us = load_user(user['user_id'])
        if form.username.data == Us.username and bcrypt.check_password_hash(Us.password, form.password.data):
            login_user(Us, remember=form.remember.data)
            flash(f"Logged {user['name']} in successfully!", 'success')
            redirect(url_for('users.home'))
        elif form.username.data == Us.username:
            if not bcrypt.check_password_hash(Us.password, form.password.data):
                flash('Login Unsuccessful. Incorrect password.', 'danger')
        else:
            flash('These username is not registered. Please register before login.', 'danger')
    return render_template('login.html',title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.home'))