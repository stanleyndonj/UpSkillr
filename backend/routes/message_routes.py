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

@message_blueprint.route("/messages", methods=["GET"])
def get_messages():
    try:
        # Retrieve messages, optionally filter by sender/receiver
        sender_id = request.args.get('sender_id')
        receiver_id = request.args.get('receiver_id')
        
        # Base query
        query = Message.query
        
        # Add filters if sender or receiver specified
        if sender_id:
            query = query.filter(Message.sender_id == sender_id)
        if receiver_id:
            query = query.filter(Message.receiver_id == receiver_id)
        
        # Order by most recent first
        messages = query.order_by(Message.timestamp.desc()).limit(100).all()
        
        # Convert messages to a list of dictionaries
        messages_list = [{
            'id': msg.id,
            'sender_id': msg.sender_id,
            'receiver_id': msg.receiver_id,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages]
        
        return jsonify(messages_list), 200
    
    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500

@message_blueprint.route("/messages/between", methods=["GET"])
def get_messages_between_users():
    try:
        sender_id = request.args.get('sender_id')
        receiver_id = request.args.get('receiver_id')
        
        if not sender_id or not receiver_id:
            return jsonify({"error": "Both sender_id and receiver_id are required"}), 400
        
        # Get messages where sender is one user and receiver is the other, in either direction
        messages = Message.query.filter(
            ((Message.sender_id == sender_id) & (Message.receiver_id == receiver_id)) |
            ((Message.sender_id == receiver_id) & (Message.receiver_id == sender_id))
        ).order_by(Message.timestamp.asc()).all()
        
        messages_list = [{
            'id': msg.id,
            'sender_id': msg.sender_id,
            'receiver_id': msg.receiver_id,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages]
        
        return jsonify(messages_list), 200
    
    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500