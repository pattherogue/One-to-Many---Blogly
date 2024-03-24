from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension  # Importing the DebugToolbarExtension
from models import db, connect_db, User, Post  # Importing SQLAlchemy database and models

app = Flask(__name__)  # Creating Flask application instance
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"  # Configuring database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disabling tracking modifications for SQLAlchemy
app.config['SECRET_KEY'] = 'ihaveasecret'  # Setting secret key for session security

# Uncomment the following line if you want to turn off Debug Toolbar intercepting redirects
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)  # Initializing DebugToolbarExtension with Flask app

connect_db(app)  # Connecting the database to Flask app

with app.app_context():
    db.create_all()  # Creating all database tables defined in models

# Route for the homepage, displaying recent posts
@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)

# Error handler for 404 NOT FOUND
@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""
    return render_template('404.html'), 404

# User routes

# Route for displaying all users
@app.route('/users')
def users_index():
    """Show a page with info on all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

# Route for showing the form to create a new user
@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Show a form to create a new user"""
    return render_template('users/new.html')

# Route for handling form submission to create a new user
@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")
    return redirect("/users")

# Route for displaying info on a specific user
@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show a page with info on a specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

# Route for showing the form to edit an existing user
@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

# Route for handling form submission to update an existing user
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")
    return redirect("/users")

# Route for handling form submission to delete an existing user
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")
    return redirect("/users")

# Posts routes

# Route for showing the form to create a new post for a specific user
@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)

# Route for handling form submission to create a new post for a specific user
@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")
    return redirect(f"/users/{user_id}")

# Route for showing info on a specific post
@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info on a specific post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

# Route for showing the form to edit an existing post
@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

# Route for handling form submission to update an existing post
@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")
    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)  # Fetches the post with the given post_id from the database. If not found, returns a 404 error.

    db.session.delete(post)  # Deletes the post object from the database session.
    db.session.commit()  # Commits the transaction to permanently delete the post from the database.

    flash(f"Post '{post.title} deleted.")  # Flashes a message indicating that the post has been successfully deleted.

    return redirect(f"/users/{post.user_id}")  # Redirects the user to the user detail page associated with the deleted post.

if __name__ == '__main__':
    app.run(debug=True)