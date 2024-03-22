from flask import Flask, render_template, send_from_directory, request, jsonify, session, redirect, url_for
from flask_sslify import SSLify
from flask_sqlalchemy import SQLAlchemy
import pytz
import ssl
import config
import hashlib

# Initialize Flask app
app = Flask(__name__, static_url_path='/data/', static_folder='./data/')
app.secret_key = 'your_secret_key'  # Change this to a random value in production

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kulka34@localhost:3306/website'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the SQLAlchemy models

#User Account Info Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

####################

# SQL Script
    #CREATE TABLE users (
    #id INTEGER PRIMARY KEY,
    #username VARCHAR(100) UNIQUE NOT NULL,
    #email VARCHAR(100) UNIQUE NOT NULL,
    #password_hash VARCHAR(128) NOT NULL,
    #created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #);

           
#User Profile Info Model
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

########

#####################

# SQL Script
    #CREATE TABLE user_profiles (
    #id INTEGER PRIMARY KEY,
    #user_id INTEGER NOT NULL,
    #full_name VARCHAR(100),
    #age INTEGER,
    #town VARCHAR(100),
    #hobby VARCHAR(100),
    #bio TEXT,
    #FOREIGN KEY (user_id) REFERENCES users(id)
    #);


# Route for Account Creation
@app.route("/join", methods=["GET"])
def newAccount():
    return render_template('./account/account_creation_form.html')
    
# Route for creating a new user account
@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    # Validate input data
    if not (username and password and email):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({"error": "Username or email already exists"}), 400

        # Hash the password before saving
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Save the new user to the database
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success": "Account created successfully"}), 200

    except Exception as e:
        # Handle any exceptions that might occur during database operations
        db.session.rollback()  # Rollback changes in case of error
        return jsonify({"error": str(e)}), 500
#######


# Route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not (username and password):
            return jsonify({"error": "Missing username or password"}), 400

        user = User.query.filter_by(username=username).first()

        # Ensure user exists and password matches
        if not user or not user.check_password(password):
            # Adding some delay here to mitigate timing attacks
            hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 100000)
            return jsonify({"error": "Invalid username or password"}), 401

        # Store the user's ID in the session to indicate they are logged in
        session['user_id'] = user.id
        return render_template('./account/ucp.html')

    elif request.method == "GET":
        # Handle GET request for login page
        return render_template('./account/account_login_form.html')

@app.route("/logout", methods=["GET", "POST"])
def logout():
    # Remove the user ID from the session if it exists
    session.pop('user_id', None)
    
    # Print message in the console
    print("User logged out successfully.")
    
    return render_template("./account/account_logout.html")

    
# Route for the User Control Panel
@app.route("/account/ucp", methods=["GET"])
def ucp():
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Fetch the user's information from the database using user_id
    user_id = session.get('user_id')
    print("User ID from session:", user_id)  # Debug statement

    user = User.query.get(user_id)
    print("User from database:", user)  # Debug statement

    if user:
        # Pass the user's information to the template
        return render_template('./account/ucp.html', username=user.username)
    else:
        return "User not found"
        
        
# Route for the Admin Control Panel
@app.route("/account/acp")
def acp():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('./account/acp.html')
    
# Route for the Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Route for the Contact Page
@app.route('/contact')
def contact():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template("contact.html")

# Route to serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('.', 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
# Error handling for 404 Not Found errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('./error/404.html'), 404

# Error handling for 500 Internal Server errors
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('./error/500.html'), 500

# Set the time zone to London
london_tz = pytz.timezone('Europe/London')
app.config['TIMEZONE'] = london_tz

# Enable HTTPS with SSLify
sslify = SSLify(app)

if __name__ == '__main__':
    # Create SSL context for HTTPS
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(config.SSL_CERTIFICATE, keyfile=config.SSL_PRIVATE_KEY, password=config.SSL_PASSPHRASE)
    
    # Run Flask app
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT, ssl_context=ssl_context)
