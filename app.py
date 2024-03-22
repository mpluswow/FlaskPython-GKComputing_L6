#
## app.py
#
from flask import Flask, render_template, send_from_directory, request, jsonify, session, redirect, url_for
from flask_sslify import SSLify  # SSLify is used for enforcing HTTPS
from modules.database import db, configure_database, User, UserProfile, PageTitle  # Import database-related modules
from modules.restricted_routes import restricted_routes  # Import restricted_routes blueprint
from modules.routes import routes
from datetime import datetime, timedelta
import pytz  # pytz for time zone handling
import ssl  # ssl for SSL certificate handling
import config  # Import configuration file
import hashlib  # hashlib for password hashing

# Initialize Flask app
app = Flask(__name__, static_url_path='/data/', static_folder='./data/')
app.secret_key = 'your_secret_key'  # Secret key for session management. Change in production.

# Register restricted_routes blueprint
app.register_blueprint(restricted_routes)
app.register_blueprint(routes)

# Configure database
configure_database(app)

# Set the time zone to London
london_tz = pytz.timezone('Europe/London')
app.config['TIMEZONE'] = london_tz

# Enable HTTPS with SSLify
sslify = SSLify(app)

# Define app routes:

# Route for fetching a single page title by ID
@app.route("/get_title/<int:page_id>", methods=["GET"])
def get_title(page_id):
    page_title = PageTitle.query.filter_by(page_id=page_id).first()
    if page_title:
        return jsonify({"title": page_title.title}), 200
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


if __name__ == '__main__':
    # Create SSL context for HTTPS
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(config.SSL_CERTIFICATE, keyfile=config.SSL_PRIVATE_KEY, password=config.SSL_PASSPHRASE)
    
    # Run Flask app
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT, ssl_context=ssl_context)
