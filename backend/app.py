from flask import Flask, jsonify, request, session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from models import db, User, Skill, SkillRequest, Review, Message  # Import all models
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from routes.auth_routes import auth_blueprint


# Initialize app and extensions
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_key'

CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "http://127.0.0.1:3000"
        ],
        "methods": ["OPTIONS", "GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize db, bcrypt, and migrate
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Create app function (needed for seeding)
def create_app():
    return app


# User registration
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username, email, password = data.get('username'), data.get('email'), data.get('password')
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

# Protected route example
@app.route('/protected', methods=['GET'])
def protected():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401
    return jsonify({'message': 'Welcome to the protected route'}), 200

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
    app.run(debug=True)
