# -*- coding: utf-8 -*-
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import redis_store, db
from flask_login import UserMixin
from . import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique = True )
    username = db.Column(db.String(64), unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError(u'你竟然想读取密码！')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    summary = db.Column(db.Text)
    count = db.Column(db.Integer, default = 0, index = True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    category = db.relationship('Category',
                                foreign_keys=[category_id],
                                backref = db.backref('posts', lazy = 'dynamic'))

    def __repr__(self):
        return '<Post %s Author %s>' % (self.title, self.author.username)


class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    count = db.Column(db.Integer, default=0, index=True)

    def __repr__(self):
        return self.name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
