from flask import Blueprint, request, jsonify
from models import User, db

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({"username": user.username, "skills_offered": user.skills_offered, "skills_requested": user.skills_requested})

@user_blueprint.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.skills_offered = data.get('skills_offered', user.skills_offered)
    user.skills_requested = data.get('skills_requested', user.skills_requested)
    db.session.commit()
    return jsonify({"message": "Profile updated successfully!"})
