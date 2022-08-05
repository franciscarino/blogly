"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import DEFAULT_IMAGE_URL, db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


############## USER ##############

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
    return render_template('detail.html', user=user, posts=user.posts)


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


############## POST ##############

@app.get('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Show new post form for user."""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new-post.html', user=user, tags=tags)


@app.post('/users/<int:user_id>/posts/new')
def handle_show_post_form(user_id):
    """Submit new post and return to user detail page."""

    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tag_id')

    new_post = Post(title=title,
                    content=content,
                    user_id=user_id,
                    created_at=None)


    db.session.add(new_post)
    db.session.commit()
    posttags = [ PostTag(post_id=new_post.id, tag_id=int(tag)) for tag in tags ]

    db.session.add_all(posttags)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.get('/posts/<int:post_id>')
def show_post_detail(post_id):
    """Show post detail page."""

    post = Post.query.get_or_404(post_id)
    return render_template('post-detail.html', post=post)

@app.get('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Show edit post form."""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit-post.html', post=post, tags=tags)

@app.post('/posts/<int:post_id>/edit')
def handle_edit_post_form(post_id):
    """Handle editing of a post. Redirect back to post view."""

    post = Post.query.get_or_404(post_id)
    title  = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tag_id')

    post.title = title
    post.content = content
    # TODO: add functionality for updating post tags in edit form
    # posttags = [ PostTag(post_id=post.id, tag_id=int(tag)) for tag in tags ]

    # for tag in tags:
    #     if


    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deletes post"""


    post = Post.query.get_or_404(post_id)
    user_id = post.user_id

    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user_id}')



############## TAGS ##############

@app.get('/tags')
def list_tags():
    """List all tags """

    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)


@app.get('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Show detail about a tag."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag-details.html', tag = tag)


@app.get('/tags/new')
def show_new_tag_form():

    return render_template('create-tag.html')


@app.post('/tags/new')
def handle_new_tag():
    """Process add form, adds tag, and redirect to tag list."""

    tag_name = request.form['new-tag']

    new_tag = Tag(name = tag_name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.get('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show edit tag form."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit-tag.html', tag=tag)

@app.post('/tags/<int:tag_id>/edit')
def handle_edit_tag_form(tag_id):
    """Handle edit tag form."""

    tag = Tag.query.get_or_404(tag_id)
    name = request.form['name']
    tag.name = name
    db.session.commit()

    return redirect(f'/tags/{tag.id}')

@app.post('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """Delete a tag."""

    Tag.query.filter(Tag.id == tag_id).delete()
    db.session.commit()

    return redirect('/tags')