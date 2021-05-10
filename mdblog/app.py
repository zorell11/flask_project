from flask import Flask
from flask import render_template
from .database import articles
from flask import request, session
from flask import redirect, url_for


flask_app = Flask(__name__)
flask_app.secret_key = b'\xae\n.\t\x05/\x91_Q\x99V\xef\x8e\x19\x04X\xe9\xb8\xc5+\x02\xec4\xc8'

@flask_app.route('/')
def view_welcome_page():
    return render_template("welcome_page.jinja")


@flask_app.route('/about')
def view_about():
    return render_template("about.jinja")


@flask_app.route('/admin')
def view_admin():
    if 'logged' not in session:
        return render_template("login.jinja")
    return render_template("admin.jinja")

@flask_app.route('/articles')
def view_articles():
    return render_template("articles.jinja", articles=articles)

@flask_app.route('/article/<int:art_id>')
def view_article(art_id):
    article = articles.get(art_id)
    if article:
        return render_template("article.jinja", article=article)
    return render_template("article_not_found.jinja", art_id=art_id)


@flask_app.route("/login/", methods=["GET"])
def view_login():
    return render_template("login.jinja")

@flask_app.route("/login/", methods=["POST"])
def login_user():
    print('#####')
    print(request)
    print('#####')
    print(request.form)
    if request.form['username'] == 'admin' and request.form['password'] == 'admin':
        session['logged'] = True
        print(session)
        return render_template("admin.jinja")
    return render_template("login.jinja")


@flask_app.route('/logout', methods=['POST'])
def view_logout():
    print(session)
    session.pop('logged')
    return redirect(url_for("view_welcome_page"))