from app.main import main
from flask import g, url_for, render_template


@main.route('/')
def index():
    return "Hello World"
