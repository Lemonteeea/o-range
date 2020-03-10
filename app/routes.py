from app import app
from flask import render_template,flash,redirect,url_for
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import MusicselectForm
from app.forms import BlogForm
from app.forms import BlogdeleteForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User,Blog
from werkzeug.urls import url_parse
from flask import request
from app import db
from datetime import datetime

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
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('username/password error')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('user',username = user.username)
        return redirect(next_page)
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
        db.session.add(user)
        db.session.commit()
        flash('恭喜你，注册成功！')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/user/<username>')
@login_required
def user(username):

    user = User.query.filter_by(username = username).first_or_404()
    blog = user.blog.all()

    return render_template('user.html', user = user , blog = blog)

@app.route('/music',methods = ['Get','Post'])
def music():
    form = MusicselectForm()
    music = form.music.data
    if form.validate_on_submit():
        return render_template('music.html', title = 'Musics', form = form, music = music)
    return render_template('music.html', title = 'Musics', form=form, music = 'kblk')

@app.route('/newblog',methods = ['Get','Post'])
@login_required
def newblog():
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blog(title = form.title.data, body = form.body.data, author = current_user)
        db.session.add(blog)
        db.session.commit()
        flash('Blog posted successfully')
    return render_template('new_blog.html', title = 'Edit Blog', form = form)


@app.route('/delete_blog/<blog_id>')
def deleteblog(blog_id):
    blog = Blog.query.filter_by(id = blog_id).first()
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('blog'))

@app.route('/blog')
def blog():
    blog = Blog.query.all()
    return render_template('list_blog.html', title='Blog', blog = blog )

@app.route('/read/<blog_id>')
def read(blog_id):
    blog = Blog.query.filter_by(id = blog_id).first()
    db.session.commit()
    return render_template('read_blog.html', title='Read', blog = blog )

@app.route('/comingsoon',methods = ['Get','Post'])
def comingsoon():
    return render_template('comingsoon.html', title = 'Comingsoon')

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.errorhandler(404)
def not_found_error(errot):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'),500
