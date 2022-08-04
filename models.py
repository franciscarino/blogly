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
        db.DateTime, nullable=False, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    tags = db.relationship('Tag', secondary='post_tags', backref='posts')


class Tag(db.Model):
    """Tags for posts."""

    __tablename__ = "tags"

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(
        db.String(20), nullable=False, unique=True)


class PostTag(db.Model):
    """Relationships between tags and posts."""

    __tablename__ = "post_tags"

    post_id = db.Column(
        db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(
        db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    # tag = db.relationship('Tag', backref='posts')