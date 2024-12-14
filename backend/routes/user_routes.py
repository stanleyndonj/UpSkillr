from flask import Blueprint, request, jsonify
from flask_cors import CORS  # Import CORS
from models import User, db
from sqlalchemy.exc import SQLAlchemyError

user_blueprint = Blueprint('user', __name__)
CORS(user_blueprint)  # Enable CORS for the user routes blueprint

@user_blueprint.route('/profile/<int:user_id>', methods=['OPTIONS'])
def options_profile(user_id):
    return '', 200  # Handle preflight request successfully


@user_blueprint.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({
            "username": user.username,
            "skills_offered": user.skills_offered,
            "skills_requested": user.skills_requested
        })
    except Exception as e:
        return jsonify({
            "error": "Error retrieving profile", 
            "details": str(e)
        }), 500

@user_blueprint.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.json
    
    if not data:
        return jsonify({"error": "No input data provided."}), 400

    try:
        user = User.query.get_or_404(user_id)

        skills_offered = data.get('skills_offered')
        skills_requested = data.get('skills_requested')

        if skills_offered and not isinstance(skills_offered, str):
            return jsonify({"error": "Skills offered must be a comma-separated string."}), 400

        if skills_requested and not isinstance(skills_requested, str):
            return jsonify({"error": "Skills requested must be a comma-separated string."}), 400

        if skills_offered:
            user.skills_offered = skills_offered
        if skills_requested:
            user.skills_requested = skills_requested

        db.session.commit()
        
        return jsonify({
            "message": "Profile updated successfully!", 
            "updated_fields": list(filter(None, ['skills_offered', 'skills_requested']))
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error occurred.", 
            "details": str(e)
        }), 500
