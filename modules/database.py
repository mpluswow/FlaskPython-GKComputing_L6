#
## database.py
#
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for database management
import hashlib  # hashlib for password hashing

# Initialize SQLAlchemy
db = SQLAlchemy()

# Function to configure database
def configure_database(app):
    # Set database connection URI and other configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kulka34@localhost:3306/website'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
# Define the SQLAlchemy models

# User Account Info Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def set_password(self, password):
        # Hash the password before storing in the database
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        # Check if the provided password matches the stored hashed password
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Define additional fields for user profile
    full_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    town = db.Column(db.String(100))
    hobby = db.Column(db.String(100))
    bio = db.Column(db.Text)
    email = db.Column(db.String(100))  # Add this line if email is not defined


class PageTitle(db.Model):
    __tablename__ = 'page_titles'  # Specify the correct table name
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    
# Define a model for pet reports
class PetReport(db.Model):
    __tablename__ = 'pet_reports'  # Specify the table name
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())