from flask import Flask
from flask import render_template
from .database import articles
from flask import request, session
from flask import redirect, url_for
import sqlite3
from flask import g
import os
from flask import flash

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import TextAreaField
from wtforms.validators import InputRequired



flask_app = Flask(__name__)
flask_app.config.from_pyfile("/vagrant/configs/default.py")

if 'MDBLOG_CONFIG' in os.environ:
    flask_app.config.from_envvar("MDBLOG_CONFIG")

 
 ### forms
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content")



@flask_app.route('/')
def view_welcome_page():
    return render_template("welcome_page.jinja")


@flask_app.route('/about')
def view_about():
    return render_template("about.jinja")


@flask_app.route('/admin')
def view_admin():
    if 'logged' not in session:
        flash("You must be logged in", "danger-alert")
        return redirect(url_for("view_login"))
    return render_template("admin.jinja")

@flask_app.route('/articles', methods=['GET'])
def view_articles():
    db = get_db()
    cursor = db.execute("select * from articles order by id desc")
    articles = cursor.fetchall()
    return render_template("articles.jinja", articles=articles)

@flask_app.route("/articles/new/", methods=['GET'])
def view_add_article():
    if "logged" not in session:
        return redirect(url_for("view_login"))
    form = ArticleForm()
    return render_template("article_editor.jinja", form=form)
    

@flask_app.route('/articles', methods=['POST'])
def add_article():
    add_article = ArticleForm(request.form) 
    db = get_db()
    db.execute("insert into articles (title, content) values (?, ?)", [add_article.title.data, add_article.content.data])
    db.commit()
    flash("Article added", "danger-ok")
    return redirect(url_for("view_articles"))

@flask_app.route('/article/<int:art_id>')
def view_article(art_id):
    db = get_db()
    cursor = db.execute("select * from articles where id=(?)", [art_id])
    article = cursor.fetchone()
    if article:
        return render_template("article.jinja", article=article)
    return render_template("article_not_found.jinja", art_id=art_id)

@flask_app.route('/article/<int:art_id>/edit', methods=['GET'])
def view_edit_article(art_id):
    if "logged" not in session:
        return redirect(url_for("view_login"))
    db = get_db()
    cursor = db.execute("select * from articles where id=(?)", [art_id])
    article = cursor.fetchone()
    if article:
        form = ArticleForm()
        form.title.data = article['title']
        form.content.data = article['content']
        return render_template("article_editor.jinja", form=form, article=article)
    return render_template("article_not_found.jinja", art_id=art_id)

@flask_app.route('/article/<int:art_id>', methods=['POST'])
def edit_article(art_id):
    if "logged" not in session:
        return redirect(url_for("view_login"))
    edit_form = ArticleForm(request.form)
    db = get_db()
    db.execute("update articles set title=(?), content=(?) where id=(?)", [edit_form.title.data, edit_form.content.data, art_id])
    db.commit()
    flash("Edit saved", "danger-ok")
    return redirect(url_for("view_article", art_id=art_id))

    

@flask_app.route("/login/", methods=["GET"])
def view_login():
    form = LoginForm()
    return render_template("login.jinja", form=form)

@flask_app.route("/login/", methods=["POST"])
def login_user():
    login_form = LoginForm(request.form)
    if login_form.username.data == flask_app.config['USERNAME'] and login_form.password.data == flask_app.config['PASSWORD']:
        session['logged'] = True
        flash("Login successful", "danger-ok")
        return render_template("admin.jinja")
    else:
        flash("Invalid credentials", "danger-alert")
        return render_template("login.jinja", form=login_form)


@flask_app.route('/logout', methods=['POST'])
def view_logout():
    print(session)
    session.pop('logged')
    flash('Successfully logged out', "danger-ok")
    return redirect(url_for("view_welcome_page"))


### UTILS
def connect_db():
    rv = sqlite3.connect(flask_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db=connect_db()
    return g.sqlite_db

@flask_app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


def init_db(app):
    with app.app_context():
        db = get_db()
        with open("mdblog/schema.sql", "r") as fp:
            db.cursor().executescript(fp.read())
        db.commit()