from flask import Flask
from flask import render_template

flask_app = Flask(__name__)

@flask_app.route('/')
def welcome_page():
    return render_template("welcome_page.jinja")


@flask_app.route('/about')
def about():
    return render_template("about.jinja")