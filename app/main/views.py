from flask import render_template, session, redirect, url_for, current_app
from . import main

@main.route('/')
def index():
    return "<h1>Hello World!</h1>"
