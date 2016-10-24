# -*- coding:utf-8 -*-
from flask import render_template, session, redirect, url_for, current_app, flash
from . import main
from .. import db
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required, \
    current_user
from ..models import User


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('.index'))
        flash(u'欢迎回来！')
    return render_template('login.html', form = form)

@main.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login'))
    return render_template('register.html', form = form)

@main.route('/post/<int:id>', methods = ['GET', 'POST'])
def post(id):
    return render_template('post.html')

@main.route('/edit-post', methods = ['GET', 'POST'])
def edit_post():
    return render_template('edit_post.html')
