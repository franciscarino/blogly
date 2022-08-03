"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')
def list_users():
    """List users"""

    users = User.query.all()
    return render_template("list.html", users=users)

@app.get('/createuser')
def create_user_form():
    """Displays form to add a new user"""

    return render_template('form.html')

@app.post('/submituser')
def submit_user():
    """Form to create a new user"""


    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img_url = request.form['img-url']
    img_url = img_url if img_url else None

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    img_url=img_url)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

