# Import necessary modules
from flask import Blueprint, render_template, jsonify, session, request
from modules.database import db, UserProfile

# Define the blueprint
update_profile_blueprint = Blueprint('update_profile', __name__)

# Route to render the update profile form
@update_profile_blueprint.route('/account/update_profile_form')
def update_profile_page():
    return render_template('account/update_profile.html') 

# Route to handle updating user profile
@update_profile_blueprint.route("/account/update_profile", methods=["POST"])
def update_profile():
    # Check if the user is logged in
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401
    
    # Retrieve data from the request
    user_id = session.get('user_id')  # Fetch user_id from session
    full_name = request.form.get("full_name")
    age = request.form.get("age")
    town = request.form.get("town")
    
    # Update user profile in the database
    user_profile = UserProfile.query.filter_by(user_id=user_id).first()
    if user_profile:
        user_profile.full_name = full_name
        user_profile.age = age
        user_profile.town = town
        db.session.commit()
        return jsonify({"message": "User profile updated successfully"}), 200
    else:
        return jsonify({"error": "User profile not found"}), 404
