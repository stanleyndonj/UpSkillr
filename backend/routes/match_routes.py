from flask import Blueprint, jsonify
from models import User

match_blueprint = Blueprint('match', __name__)

@match_blueprint.route('/match/<int:user_id>', methods=['GET'])
def find_matches(user_id):
    user = User.query.get_or_404(user_id)

    if not user.skills_requested:
        return jsonify({"error": "User has no skills requested specified."}), 400

    matches = User.query.filter(User.skills_offered.in_(user.skills_requested.split(','))).all()
    match_list = [{"id": match.id, "username": match.username, "skills_offered": match.skills_offered} for match in matches]

    return jsonify({"matches": match_list}), 200
