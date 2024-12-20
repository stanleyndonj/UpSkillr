from flask import Blueprint, jsonify, request
from models import User
from sqlalchemy import func

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
        user = User.query.get_or_404(user_id)
        
        # Check if user has skills_requested
        if not user.skills_requested:
            return jsonify({"error": "User has no skills requested specified."}), 400
        
        # Split skills by comma, strip whitespace, and ignore empty entries
        requested_skills = [skill.strip() for skill in user.skills_requested.split(',') if skill.strip()]
        
        # If no valid skills, return an error
        if not requested_skills:
            return jsonify({"error": "No valid skills found."}), 400
        
        # Perform a case-insensitive match for skills offered
        matches = User.query.filter(
            func.lower(User.skills_offered).in_([func.lower(skill) for skill in requested_skills])
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        # Format the matches to return relevant data
        match_list = [
            {
                "id": match.id, 
                "username": match.username, 
                "skills_offered": match.skills_offered
            } for match in matches.items
        ]
        
        # Return the matches with pagination info
        return jsonify({
            "matches": match_list,
            "total_matches": matches.total,
            "page": page,
            "per_page": per_page
        }), 200
    
    except Exception as e:
        # Log the error and return a generic message to the client
        return jsonify({"error": "Match search failed", "details": str(e)}), 500
