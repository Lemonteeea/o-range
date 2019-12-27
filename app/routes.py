from app import app
from flask import render_template,flash,redirect,url_for
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import MusicselectForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User
from werkzeug.urls import url_parse
from flask import request
from app import database

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = 'Home Page')

@app.route('/login',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first_or_404()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        return redirect(url_for('user', username = form.username.data))
    return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods = ['Get', 'Post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        database.session.add(user)
        database.session.commit()
        flash('恭喜你，注册成功！')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    posts = [
            {'author': user, 'body': 'Test post #1'},
            {'author': user, 'body': 'Test post #2'}
            ]
    return render_template('user.html', user = user , posts = posts)

@app.route('/music',methods = ['Get','Post'])
def music():
    form = MusicselectForm()
    music = form.music.data
    if form.validate_on_submit():
        return render_template('music.html', title = 'Musics', form=form, music = music)
    return render_template('music.html', title = 'Musics', form=form, music = 'kblk')

@app.route('/comingsoon',methods = ['Get','Post'])
def comingsoon():
    return render_template('comingsoon.html', title = 'Comingsoon')

