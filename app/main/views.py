# -*- coding:utf-8 -*-
from flask import request, render_template, session, redirect, url_for, current_app, flash
from . import main
from .. import db
from .forms import LoginForm, RegistrationForm, EditPostForm, PostForm, CategoryForm
from flask_login import login_user, logout_user, login_required, \
    current_user
from ..models import User, Post, Category


@main.route('/', methods = ['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('index.html', posts = posts)


@main.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash(u'欢迎回来！')
            return redirect(url_for('.index'))
        else:
            flash(u"用户名或密码错误，请重试")
    return render_template('login.html', form = form)


@main.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    flash(u'你已退出登录。')
    return redirect(url_for('.index'))


@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


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


@main.route('/secret')
@login_required
def secret():
    return u'只有已登录用户可见!'



@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts = [post])


@main.route('/category', methods=['GET', 'POST'])
def category():
    categories = Category.query.all()
    return render_template('category.html', categories = categories)


@main.route('/category/delete/<int:cat_id>', methods=['GET', 'POST'])
def category_delete(cat_id):
    category = Category.query.filter_by(id=cat_id).first()
    category.delete()
    flash(u'栏目已删除')
    return redirect(url_for('main.category'))


@main.route('/edit-post', methods=['GET', 'POST'])
@login_required
def edit_post():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit:
        post = Post(title = form.title.data,
                    author = current_user,
                    body = form.body.data,
                    category = Category.query.filter_by(id = form.category.data).first())
        db.session.add(post)
        db.session.commit()
        flash(u'发布成功！')
        return redirect(url_for('.post', id = post.id))
    return render_template('edit_post.html', form = form)
