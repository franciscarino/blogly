"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
db = SQLAlchemy()

DEFAULT_IMAGE_URL = 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/gettyimages-1144982182.jpg'

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Blogly User table"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,primary_key=True, autoincrement=True)
    first_name = db.Column(
        db.String(50), nullable=False, unique=False)
    last_name = db.Column(
        db.String(50), nullable=False, unique=False)
    img_url = db.Column(db.Text, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref='user')


class Post(db.Model):
    """Posts per User"""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(
        db.String(50), nullable=False, unique=False)
    content = db.Column(
        db.Text, nullable=True, unique=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


