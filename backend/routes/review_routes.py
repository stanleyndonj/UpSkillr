from flask import Blueprint, request, jsonify
from models import Review, User, db
from sqlalchemy.exc import SQLAlchemyError

review_blueprint = Blueprint('review', __name__)

@review_blueprint.route('/review', methods=['POST'])
def add_review():
    data = request.json
    
    # Input validation
    if not data:
        return jsonify({"error": "No input data provided."}), 400

    # Check for required fields
    required_fields = ['user_id', 'rating', 'comment']
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields. Required: {required_fields}"}), 400

    try:
        # Validate user existence
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({"error": "User not found."}), 404

        # Enhanced rating validation
        rating = data['rating']
        if not isinstance(rating, (int, float)) or rating < 1 or rating > 5:
            return jsonify({"error": "Rating must be a number between 1 and 5."}), 400

        # Comment length validation
        comment = data['comment']
        if len(comment) > 500:  # Example max length
            return jsonify({"error": "Comment too long. Max 500 characters."}), 400

        # Create and save review
        review = Review(
            user_id=data['user_id'], 
            rating=rating, 
            comment=comment
        )
        
        db.session.add(review)
        db.session.commit()

        return jsonify({
            "message": "Review added successfully!", 
            "review_id": review.id
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error occurred.", 
            "details": str(e)
        }), 500