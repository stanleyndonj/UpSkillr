<<<<<<< HEAD
from flask import Blueprint, request, jsonify, make_response, current_app, session
=======
from flask import Blueprint, request, jsonify, make_response
>>>>>>> 0a50b5d294b5cab8bdc98d8d3c218f07e313c491
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
import jwt
import datetime
import re
from flask import current_app

auth_blueprint = Blueprint('auth', __name__)

<<<<<<< HEAD
@auth_blueprint.route('/signup', methods=['OPTIONS'])
def signup_options():
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

@auth_blueprint.route('/login', methods=['OPTIONS'])
def login_options():
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

=======
>>>>>>> 0a50b5d294b5cab8bdc98d8d3c218f07e313c491
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

<<<<<<< HEAD
@auth_blueprint.route('/signup', methods=['POST'])
=======
@auth_blueprint.route('/login', methods=['POST', 'OPTIONS'])
def login():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.status_code = 200
        return response 

    # Handle POST request
    data = request.json 

    if not data:
        return jsonify({'error': 'No input data provided'}), 400 

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400 

    # Find user
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid username or password'}), 401 

    # Create JWT token
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    # Modify response to include CORS headers
    response = make_response(jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200)
    
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@auth_blueprint.route('/signup', methods=['OPTIONS', 'POST'])
>>>>>>> 0a50b5d294b5cab8bdc98d8d3c218f07e313c491
def signup():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.status_code = 200
        return response 

    # Handle POST request
    data = request.json 

    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'error': 'Missing required fields: username, email, and password.'}), 400

    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format.'}), 400

    if User.query.filter((User.email == data['email']) | (User.username == data['username'])).first():
        return jsonify({'error': 'Username or email already exists.'}), 409

    if len(data['password']) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long.'}), 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=16)
    user = User(username=data['username'], email=data['email'], password_hash=hashed_password)

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        db.session.rollback()
<<<<<<< HEAD
        return jsonify({"error": "Registration failed", "details": str(e)}), 500

# User login
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json

    # Validate input data
    if not all(k in data for k in ('email', 'password')):
        return jsonify({"error": "Missing required fields: email and password."}), 400

    email = data['email']
    password = data['password']

    # Check if user exists
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Invalid credentials."}), 401

    # Check if password is correct
    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials."}), 401

    # Create a JWT token
    token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    # Optionally store the user ID in the session (if using sessions)
    session['user_id'] = user.id

    return jsonify({"message": "Login successful", "token": token}), 200
=======
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500

@auth_blueprint.route('/verify', methods=['GET'])
def verify_token():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'valid': False}), 401

    try:
        # Remove 'Bearer ' from token
        token = token.split(' ')[1]
        
        # Decode the token
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Find the user
        user = User.query.get(decoded['user_id'])
        
        if user:
            return jsonify({
                'valid': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
        else:
            return jsonify({'valid': False}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({'valid': False}), 401
    except jwt.InvalidTokenError:
        return jsonify({'valid': False}), 401
>>>>>>> 0a50b5d294b5cab8bdc98d8d3c218f07e313c491
