from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from flask_login import UserMixin, LoginManager
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"
# app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=True)
    body = db.Column(db.String(300), nullable=True)
    creates_at = db.Column(db.DateTime, nullable=False, default = datetime.now(pytz.timezone('Asia/Tokyo')).replace(second=0, microsecond=0))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(12),unique=True)


@app.route("/", methods=['GET','POST'])
def index2():
    if request.method == 'GET':
        posts = Post.query.all()
    return render_template('index2.html', posts=posts)


@app.route('/create2', methods = ["GET","POST"])
def create2():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        post = Post(title=title, body=body)

        db.session.add(post)
        db.session.commit()
        return redirect('/')

    else:
        return render_template('create2.html')



# @app.route('/<int:id>/update', methods = ["GET","POST"])
# def update(id):
#     id = Post.query.get(id)
#     if request.method == 'POST':
#         id.title = request.form.get('title')
#         id.body = request.form.get('body')

#         db.session.commit()
#         return redirect('/')

#     else:
#         return render_template('update.html', post=id)

@app.route('/<int:id>/update2', methods = ["GET","POST"])
def update2(id):
    id = Post.query.get(id)
    if request.method == 'POST':
        id.title = request.form.get('title')
        id.body = request.form.get('body')

        db.session.commit()
        return redirect('/')

    else:
        return render_template('update2.html', post=id)

@app.route('/<int:id>/delete')
def delete(id):
    id = Post.query.get(id)

    db.session.delete(id)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

