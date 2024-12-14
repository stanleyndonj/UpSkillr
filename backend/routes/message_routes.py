from flask import Blueprint, request, jsonify
from models import db, User, Message
from sqlalchemy.exc import SQLAlchemyError

message_blueprint = Blueprint("message", __name__)

@message_blueprint.route("/messages", methods=["POST"])
def send_message():
    data = request.json
    
    # More robust input validation
    if not data:
        return jsonify({"error": "No input data provided."}), 400
    
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    content = data.get("content")

    # Comprehensive validation
    if not all([sender_id, receiver_id, content]):
        return jsonify({"error": "All fields (sender_id, receiver_id, content) are required."}), 400

    # Validate that sender and receiver are different
    if sender_id == receiver_id:
        return jsonify({"error": "Sender and receiver cannot be the same user."}), 400

    try:
        sender = User.query.get(sender_id)
        receiver = User.query.get(receiver_id)

        if not sender or not receiver:
            return jsonify({"error": "Sender or Receiver not found."}), 404

        # Length validation for message content
        if len(content) > 1000:  # Example max length
            return jsonify({"error": "Message content too long. Max 1000 characters."}), 400

        message = Message(
            sender_id=sender_id, 
            receiver_id=receiver_id, 
            content=content
        )
        
        db.session.add(message)
        db.session.commit()

        return jsonify({
            "message": "Message sent successfully.", 
            "message_id": message.id
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error occurred.", 
            "details": str(e)
        }), 500