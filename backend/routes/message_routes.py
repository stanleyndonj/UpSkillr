from flask import Blueprint, request, jsonify
from models import db, User, Message

message_blueprint = Blueprint("message", __name__)

@message_blueprint.route("/messages", methods=["POST"])
def send_message():
    """
    Send a new message from one user to another.
    Request body should include: sender_id, receiver_id, content.
    """
    data = request.json
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    content = data.get("content")

    if not (sender_id and receiver_id and content):
        return jsonify({"error": "All fields (sender_id, receiver_id, content) are required."}), 400

    sender = User.query.get(sender_id)
    receiver = User.query.get(receiver_id)

    if not sender or not receiver:
        return jsonify({"error": "Sender or Receiver not found."}), 404

    message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(message)
    db.session.commit()

    return jsonify({"message": "Message sent successfully.", "message_id": message.id}), 201

@message_blueprint.route("/messages/<int:sender_id>/<int:receiver_id>", methods=["GET"])
def get_conversation(sender_id, receiver_id):
    """
    Retrieve the conversation between two users.
    """
    sender = User.query.get(sender_id)
    receiver = User.query.get(receiver_id)

    if not sender or not receiver:
        return jsonify({"error": "Sender or Receiver not found."}), 404

    messages = Message.query.filter(
        ((Message.sender_id == sender_id) & (Message.receiver_id == receiver_id)) |
        ((Message.sender_id == receiver_id) & (Message.receiver_id == sender_id))
    ).order_by(Message.timestamp).all()

    conversation = [
        {
            "id": message.id,
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id,
            "content": message.content,
            "timestamp": message.timestamp
        } for message in messages
    ]

    return jsonify({"conversation": conversation}), 200

@message_blueprint.route("/messages/<int:user_id>", methods=["GET"])
def get_user_messages(user_id):
    """
    Retrieve all messages sent to or from a user.
    """
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found."}), 404

    messages = Message.query.filter(
        (Message.sender_id == user_id) | (Message.receiver_id == user_id)
    ).order_by(Message.timestamp).all()

    user_messages = [
        {
            "id": message.id,
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id,
            "content": message.content,
            "timestamp": message.timestamp
        } for message in messages
    ]

    return jsonify({"messages": user_messages}), 200
