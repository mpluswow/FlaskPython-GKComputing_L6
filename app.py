from flask import Flask, render_template, send_from_directory, jsonify, session, request
from flask_sslify import SSLify
from modules.database import db, configure_database, UserProfile, PageTitle, PetReport
from modules.restricted_routes import restricted_routes
from modules.routes import routes
from modules.profile_routes import update_profile_blueprint
from datetime import datetime, timedelta
import pytz
import ssl
import config

# Initialize Flask app
app = Flask(__name__, static_url_path='/data/', static_folder='./data/')
app.secret_key = 'your_secret_key'  # Secret key for session management. Change in production.

# Register blueprints
app.register_blueprint(restricted_routes)
app.register_blueprint(routes)
app.register_blueprint(update_profile_blueprint)


# Configure database
configure_database(app)

# Set the time zone to London
london_tz = pytz.timezone('Europe/London')
app.config['TIMEZONE'] = london_tz

# Enable HTTPS with SSLify
sslify = SSLify(app)

# Fetch user profile function
def fetch_user_profile(user_id):
    user_profile = UserProfile.query.filter_by(user_id=user_id).first()
    return user_profile

# Route to fetch user profile
@app.route("/get_user_profile")
def get_user_profile_route():
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    user_id = session.get('user_id')
    user_profile = fetch_user_profile(user_id)

    if user_profile:
        return jsonify({
            "age": user_profile.age,
            "full_name": user_profile.full_name,
            "town": user_profile.town,
        })
    else:
        return jsonify({"error": "User profile not found"}), 404

# Route to fetch page title by ID
@app.route("/get_title/<int:page_id>", methods=["GET"])
def get_title(page_id):
    page_title = PageTitle.query.filter_by(page_id=page_id).first()
    if page_title:
        title_data = {"title": page_title.title}
        return jsonify(title_data), 200
    else:
        return jsonify({"error": "Title not found"}), 404

# Route for the Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Route to serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('.', 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
@app.route('/account/update_profile_form')
def update_profile_page():
    return render_template('account/update_profile.html') 
    
@app.route("/account/update_profile", methods=["POST", "GET"])
def update_profile():
    if request.method == "GET":
        # Handle GET request, such as rendering a form
        return render_template('update_profile_form.html')
    elif request.method == "POST":
        # Handle POST request, such as processing form data
        # Check if the user is logged in
        if 'user_id' not in session:
            return jsonify({"error": "User not logged in"}), 401
        
        # Retrieve data from the request
        user_id = session.get('user_id')  # Fetch user_id from session
        full_name = request.form.get("full_name")
        age = request.form.get("age")
        town = request.form.get("town")
        
        # Update user profile in the database
        user_profile = UserProfiles.query.filter_by(user_id=user_id).first()
        if user_profile:
            user_profile.full_name = full_name
            user_profile.age = age
            user_profile.town = town
            db.session.commit()
            return jsonify({"message": "User profile updated successfully"}), 200
        else:
            return jsonify({"error": "User profile not found"}), 404

if __name__ == '__main__':
    # Create SSL context for HTTPS
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(config.SSL_CERTIFICATE, keyfile=config.SSL_PRIVATE_KEY, password=config.SSL_PASSPHRASE)
    
    # Run Flask app
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT, ssl_context=ssl_context)