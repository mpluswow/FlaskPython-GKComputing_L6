from flask import Blueprint, request, jsonify, render_template
from .database import db, PetReport  # Import the db instance

petReport = Blueprint('petReport', __name__)


# Route for reporting a pet location
@petReport.route("/report_pet", methods=["POST"])
def report_pet():
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    description = request.form.get("description")

    # Validate input data
    if not (latitude and longitude and description):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Save the pet report to the database
        new_report = PetReport(latitude=latitude, longitude=longitude, description=description)
        db.session.add(new_report)
        db.session.commit()
        return jsonify({"message": "Pet report saved successfully"}), 200
    except Exception as e:
        # Handle any exceptions that might occur during database operations
        db.session.rollback()  # Rollback changes in case of error
        return jsonify({"error": str(e)}), 500