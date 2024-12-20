from flask import Blueprint, jsonify, request
from models import User, Skill, SkillRequest
from sqlalchemy.orm import aliased

match_blueprint = Blueprint('match', __name__)

@match_blueprint.route('/match/<int:user_id>', methods=['GET'])
def find_matches(user_id):
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Ensure per_page is not too large
    per_page = min(per_page, 100)
    
    try:
        # Fetch the user from the database
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found."}), 404
        
        # Check if user has skills_requested
        if not user.skills_requested:
            return jsonify({"error": "User has no skills requested specified."}), 400
        
        # Split skills by comma, strip whitespace, and ignore empty entries
        requested_skills = [skill.strip() for skill in user.skills_requested.split(',') if skill.strip()]
        
        # If no valid skills, return an error
        if not requested_skills:
            return jsonify({"error": "No valid skills found."}), 400
        
        # Temporarily add generic matches for testing purposes
        generic_matches = [
            {"id": i, "username": f"TestUser{i}", "skills_offered": "SkillA, SkillB"} for i in range(1, 11)
        ]
        
        # Return the generic matches and pagination info
        return jsonify({
            "matches": generic_matches,
            "total_matches": len(generic_matches),
            "page": page,
            "per_page": per_page
        }), 200
    
    except Exception as e:
        # Log the error and return a generic message to the client
        return jsonify({"error": "Match search failed", "details": str(e)}), 500
