from flask import Blueprint, request, jsonify
from models import db, User, Message

message_blueprint = Blueprint("message", __name__)

@message_blueprint.route("/messages", methods=["POST"])
def send_message():
    data = request.json
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    content = data.get("content")

    if not all([sender_id, receiver_id, content]):
        return jsonify({"error": "All fields (sender_id, receiver_id, content) are required."}), 400

    sender = User.query.get(sender_id)
    receiver = User.query.get(receiver_id)

    if not sender or not receiver:
        return jsonify({"error": "Sender or Receiver not found."}), 404

    message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(message)
    db.session.commit()

    return jsonify({"message": "Message sent successfully.", "message_id": message.id}), 201
