from flask import Blueprint, render_template, send_from_directory, request, jsonify, session, redirect, url_for
from modules.restricted_routes import restricted_routes
from modules.database import User, UserProfile

routes = Blueprint('routes', __name__)
    
# Route for Account Creation form
@routes.route("/join", methods=["GET"])
def newAccount():
    return render_template('./account/account_creation_form.html')

# Route for creating a new user account
@routes.route("/create_account", methods=["POST"])
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

# Route for user login
@routes.route("/login", methods=["GET", "POST"])
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

# Route for user logout
@routes.route("/logout", methods=["GET", "POST"])
def logout():
    # Remove the user ID from the session if it exists
    session.pop('user_id', None)
    
    # Print message in the console
    print("User logged out successfully.")
    
    return render_template("./account/account_logout.html")


# Route for the Admin Control Panel
@routes.route("/account/acp")
def acp():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('./account/acp.html')


# Error handling for 404 Not Found errors
@routes.errorhandler(404)
def not_found_error(error):
    return render_template('./error/404.html'), 404

# Error handling for 500 Internal Server errors
@routes.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('./error/500.html'), 500
    
# Route for Testing
@routes.route("/test")
def test():
    print("Rendering test.html")
    return render_template('test.html') 
