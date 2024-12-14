from flask import Blueprint, request, jsonify
from models import User, db
from sqlalchemy.exc import SQLAlchemyError

user_blueprint = Blueprint('user', __name__)

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
    
    # Input validation
    if not data:
        return jsonify({"error": "No input data provided."}), 400

    try:
        user = User.query.get_or_404(user_id)

        # Validate skills input
        skills_offered = data.get('skills_offered')
        skills_requested = data.get('skills_requested')

        # Validate skills format (assuming comma-separated strings)
        if skills_offered and not isinstance(skills_offered, str):
            return jsonify({"error": "Skills offered must be a comma-separated string."}), 400

        if skills_requested and not isinstance(skills_requested, str):
            return jsonify({"error": "Skills requested must be a comma-separated string."}), 400

        # Update profile
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