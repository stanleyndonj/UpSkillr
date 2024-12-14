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
        user = User.query.get_or_404(user_id)
        
        if not user.skills_requested:
            return jsonify({"error": "User has no skills requested specified."}), 400
        
        # Split skills and handle potential empty or None values
        requested_skills = [skill.strip() for skill in user.skills_requested.split(',') if skill.strip()]
        
        if not requested_skills:
            return jsonify({"error": "No valid skills found."}), 400
        
        # More robust matching with case-insensitive search
        matches = User.query.filter(
            func.lower(User.skills_offered).in_([skill.lower() for skill in requested_skills])
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        match_list = [
            {
                "id": match.id, 
                "username": match.username, 
                "skills_offered": match.skills_offered
            } for match in matches.items
        ]
        
        return jsonify({
            "matches": match_list,
            "total_matches": matches.total,
            "page": page,
            "per_page": per_page
        }), 200
    
    except Exception as e:
        return jsonify({"error": "Match search failed", "details": str(e)}), 500