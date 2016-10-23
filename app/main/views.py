# -*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, current_app
from . import main
from .forms import LoginForm
from flask_login import login_user, logout_user, login_required, \
    current_user
from ..models import User


@main.route('/')
def index():
    return "<h1>Hello World!</h1>"

@main.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return url_for('index')
        flash(u'欢迎回来！')
    return render_template('login.html', form = form)
