### app.py ###
from flask import Flask, jsonify, request, session, make_response
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from models import db, User, Skill
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from routes.auth_routes import auth_blueprint
import jwt

# Initialize app and extensions
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super_secret_key'

# More comprehensive CORS configuration
CORS(app, resources={r"/*": {
    "origins": [
        "https://upskillr-nis2.onrender.com", 
        "https://upskillr-nis2.onrender.com"
    ],
    "methods": ["OPTIONS", "GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True  # New line
}})

# Initialize db, bcrypt, and migrate
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Create app function (needed for seeding)
def create_app():
    return app

# Profile endpoint
@app.route('/api/profile', methods=['GET', 'OPTIONS'])
def profile():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'https://upskillr-nis2.onrender.com')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')  # New line
        response.status_code = 200
        return response 

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Missing token'}), 401 

    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded.get('user_id')
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'name': user.username,
            'email': user.email,
            'joinedDate': user.created_at.strftime('%Y-%m-%d')
        }), 200
    except Exception as e:
        return jsonify({'error': 'Invalid or expired token', 'details': str(e)}), 401

# CRUD for Skills
@app.route('/skills', methods=['GET', 'POST'])
def skills():
    if request.method == 'GET':
        skills = Skill.query.all()
        return jsonify([{'id': s.id, 'name': s.name, 'user_id': s.user_id} for s in skills]), 200
    
    if request.method == 'POST':
        data = request.get_json()
        name, user_id = data.get('name'), data.get('user_id')
        if not name or not user_id:
            return jsonify({'error': 'Missing required fields'}), 400
        
        skill = Skill(name=name, user_id=user_id)
        db.session.add(skill)
        db.session.commit()
        return jsonify({'message': 'Skill added successfully'}), 201

# Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

if __name__ == '__main__':
    # Ensure the app context is pushed for CLI operations
    with app.app_context():
        app.run(debug=True, host='0.0.0.0', port=5000)