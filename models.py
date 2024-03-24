import datetime  # Importing datetime module for date and time operations
from flask_sqlalchemy import SQLAlchemy  # Importing SQLAlchemy

# Creating an instance of the SQLAlchemy class
db = SQLAlchemy()

# Default image URL for user profile images
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

# User model definition
class User(db.Model):
    """Site user."""

    __tablename__ = "users"  # Table name in the database

    # Columns in the users table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column for user ID
    first_name = db.Column(db.Text, nullable=False)  # Column for user's first name
    last_name = db.Column(db.Text, nullable=False)  # Column for user's last name
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)  # Column for user's profile image URL

    # Relationship with posts table: One-to-many relationship where one user can have multiple posts
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    # Property to return the full name of the user
    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"

# Post model definition
class Post(db.Model):
    """Blog post."""

    __tablename__ = "posts"  # Table name in the database

    # Columns in the posts table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column for post ID
    title = db.Column(db.Text, nullable=False)  # Column for post title
    content = db.Column(db.Text, nullable=False)  # Column for post content
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)  # Column for post creation date and time

    # Foreign key referencing the users table to establish the one-to-many relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Property to return a friendly formatted date
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

# Function to connect the database to the Flask app
def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """
    db.app = app  # Setting the Flask app for the database
    db.init_app(app)  # Initializing the database with the Flask app
