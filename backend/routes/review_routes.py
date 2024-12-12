from flask import Blueprint, request, jsonify
from models import Review, User, db

review_blueprint = Blueprint('review', __name__)

@review_blueprint.route('/review', methods=['POST'])
def add_review():
    data = request.json
    user = User.query.get(data['user_id'])

    if not user:
        return jsonify({"error": "User not found."}), 404

    if not (1 <= data['rating'] <= 5):
        return jsonify({"error": "Rating must be between 1 and 5."}), 400

    review = Review(user_id=data['user_id'], rating=data['rating'], comment=data['comment'])
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review added successfully!"}), 201
