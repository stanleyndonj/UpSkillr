from flask import Blueprint, request, jsonify
from models import Review, db

review_blueprint = Blueprint('review', __name__)

@review_blueprint.route('/review', methods=['POST'])
def add_review():
    data = request.json
    review = Review(user_id=data['user_id'], rating=data['rating'], comment=data['comment'])
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review added successfully!"})
