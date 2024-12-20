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
        user = User.query.get_or_404(user_id)
        
        # Fetch skill requests made by the user
        skill_requests = SkillRequest.query.filter_by(user_id=user_id).all()
        
        if not skill_requests:
            return jsonify({"error": "User has no skill requests."}), 400
        
        # Extract skill IDs from the user's requests
        requested_skill_ids = [req.skill_id for req in skill_requests]
        
        if not requested_skill_ids:
            return jsonify({"error": "No valid skills requested."}), 400
        
        # Find users offering the requested skills
        matches = (
            User.query.join(Skill, Skill.user_id == User.id)
            .filter(Skill.id.in_(requested_skill_ids), User.id != user_id)
            .distinct()
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        
        # Format the matches
        match_list = [
            {
                "id": match.id,
                "username": match.username,
                "skills_offered": [skill.name for skill in match.skills],
            }
            for match in matches.items
        ]
        
        # Return the matches with pagination info
        return jsonify({
            "matches": match_list,
            "total_matches": matches.total,
            "page": page,
            "per_page": per_page,
        }), 200
    
    except Exception as e:
        # Log the error and return a generic message to the client
        return jsonify({"error": "Match search failed", "details": str(e)}), 500
