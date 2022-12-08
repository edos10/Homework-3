from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.Integer, default=datetime.utcnow())

    def __repr__(self):
        return '<Resume %r>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route("/")
def main():
    return redirect("/main")


@app.route("/main")
def main():
    return render_template("base.html")


@app.route("/register")
def register():
    return render_template("registration.html")


@app.route("/authorisation")
def register():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
