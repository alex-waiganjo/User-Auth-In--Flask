from flask import Blueprint,render_template,redirect,url_for,request,flash
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user ,login_required,logout_user

auth = Blueprint('auth',__name__)

@auth.route('/signup',methods=['GET','POST'])
def signup():
    #Getting user data from the form
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    #Testing whether the email exists, if it returns an email then the email already exists
    check_email = User.query.filter_by(email=email).first()

    #Redirecting the user to the signup page
    if check_email:
        flash('Sorry Email Already Exixts,Try using a different Email,or Login')
        return redirect(url_for('auth.signup'))

    #Adding user details to the db and encrypting the password
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/login',methods=['GET','POST'])
def login():
    email = request.form.get('email')
    password =request.form.get('password')
    remember =  True if request.form.get('remember') else False

    #Checking whether the email exists
    user = User.query.filter_by(email= email).first()

    #If incorrect details reload the page 
    if not user or not check_password_hash(user.password,password):
        flash('Check youy Login Details and try again')
        return redirect(url_for('auth.login'))

    login_user(user,remember=remember)    

    #Show the profile page if login is successful
    return redirect(url_for('main.profile'))


@auth.route('/logout')  
@login_required
def logout():
    logout_user()
    return   redirect(url_for('main.index'))  
    