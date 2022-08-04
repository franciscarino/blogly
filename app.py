"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import DEFAULT_IMAGE_URL, db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')
def home_page():
    """Redirects to users page"""

    return redirect('/users')

@app.get('/users')
def list_users():
    """List users"""

    users = User.query.all()
    return render_template("list.html", users=users)

@app.get('/users/new')
def create_user_form():
    """Displays form to add a new user"""

    return render_template('form.html')

@app.post('/users/new')
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
    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_details(user_id):
    """Shows user details"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id)
    return render_template('detail.html', user=user, posts=posts)


@app.get('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """Displays edit page"""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.post('/users/<int:user_id>/edit')
def submit_edit_page(user_id):
    """Submit edit details"""

    user = User.query.get_or_404(user_id)

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img_url = request.form['img-url']
    img_url = img_url if img_url else DEFAULT_IMAGE_URL

    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url


    # db.session.add(user)
    db.session.commit()
    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Handle form to delete user"""

    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/users')



@app.get('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Show new post form for user."""

    user = User.query.get_or_404(user_id)
    return render_template('new-post.html', user=user)


@app.post('/users/<int:user_id>/posts/new')
def handle_show_post_form(user_id):
    """Submit new post and return to user detail page."""

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title,
                    content=content,
                    user_id=user_id,
                    created_at=None)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.get('/posts/<int:post_id>')
def show_post_detail(post_id):
    """Show post detail page."""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    user = User.query.get(user_id)
    return render_template('post-detail.html', post=post, user=user)

@app.get('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Show edit post form."""

    post = Post.query.get_or_404(post_id)
    return render_template('edit-post.html', post=post)