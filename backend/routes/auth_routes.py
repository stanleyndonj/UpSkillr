from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
import jwt
import datetime
from flask import current_app
import re
from flask import Blueprint, request, jsonify, make_response, current_app

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
        return jsonify({"error": "Missing required fields."}), 400
    
    # Validate email format
    if not validate_email(data['email']):
        return jsonify({"error": "Invalid email format."}), 400
    
    # Check if user already exists
    existing_user = User.query.filter(
        (User.email == data['email']) | (User.username == data['username'])
    ).first()
    
    if existing_user:
        return jsonify({"error": "Username or email already exists."}), 409
    
    # Password strength (example: minimum 8 characters)
    if len(data['password']) < 8:
        return jsonify({"error": "Password must be at least 8 characters long."}), 400
    
    # Hash password with method and salt rounds
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=16)
    
    try:
        user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Registration failed", "details": str(e)}), 500

@auth_blueprint.route('/login', methods=['OPTIONS'])
def login_options():
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    
    # Validate request data
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing email or password"}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        try:
            # Updated token generation for newer PyJWT versions
            token = jwt.encode(
                {
                    'user_id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                }, 
                current_app.config['SECRET_KEY'], 
                algorithm="HS256"
            )
            return jsonify({"token": token}), 200
        except Exception as e:
            return jsonify({"error": "Token generation failed", "details": str(e)}), 500
    
    return jsonify({"message": "Invalid credentials!"}), 401