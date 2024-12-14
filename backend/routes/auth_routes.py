from flask import Blueprint, request, jsonify, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
import jwt
import datetime
import re

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['OPTIONS'])
def signup_options():
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)


@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.json

    # Validate required fields
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({"error": "Missing required fields: username, email, and password."}), 400

    # Validate email format
    if not validate_email(data['email']):
        return jsonify({"error": "Invalid email format."}), 400

    # Check if user already exists
    existing_user = User.query.filter(
        (User.email == data['email']) | (User.username == data['username'])
    ).first()

    if existing_user:
        return jsonify({"error": "Username or email already exists."}), 409

    # Password strength validation
    if len(data['password']) < 8:
        return jsonify({"error": "Password must be at least 8 characters long."}), 400

    # Hash password
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=16)

    try:
        user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Registration failed", "details": str(e)}), 500
