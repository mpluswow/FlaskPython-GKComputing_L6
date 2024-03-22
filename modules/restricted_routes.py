#
## restricted_routes.py
#
from flask import Blueprint, render_template, redirect, url_for, session
from modules.database import User

restricted_routes = Blueprint('restricted_routes', __name__)

@restricted_routes.route('/contact')
def contact():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    return render_template("contact.html")

# Route for the User Control Panel
@restricted_routes.route("/account/ucp", methods=["GET"])
def ucp():
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

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

