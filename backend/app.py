from flask import Flask, jsonify, request, session, make_response
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, User, Skill, Message
from routes.auth_routes import auth_blueprint
import jwt
print("Importing ai_routes...")
from routes.ai_routes import ai_routes
print("ai_routes imported successfully")
from openai import OpenAI
from config import Config


# Initialize app and extensions
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super_secret_key'

# Configure CORS
CORS(app, resources={r"/*": {
    "origins": ["https://upskillr-1-9xow.onrender.com"],  
    "methods": ["OPTIONS", "GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True
}})

# Initialize db, bcrypt, and migrate
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(ai_routes)



client = OpenAI(api_key=Config.OPENAI_API_KEY)


# Create app function (needed for seeding)
def create_app():
    return app

# Default OPTIONS response handler
@app.before_request
def handle_options_request():
        if request.method == "OPTIONS":
           response = make_response()
           response.headers["Access-Control-Allow-Origin"] = "https://upskillr-1-9xow.onrender.com"
           response.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST, PUT, DELETE"
           response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
           response.headers["Access-Control-Allow-Credentials"] = "true"
           return response, 200

# Profile endpoint
@app.route('/api/profile', methods=['GET'])
def profile():
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

@app.route('/messages/between', methods=['GET'])
def get_messages_between():
    user1_id = request.args.get('sender_id')
    user2_id = request.args.get('receiver_id')
    
    if not user1_id or not user2_id:
        return jsonify({'error': 'Missing user IDs'}), 400
    
    try:
        # Adjust query based on your database schema
        messages = Message.query.filter(
            (Message.sender_id == user1_id) & (Message.receiver_id == user2_id) |
            (Message.sender_id == user2_id) & (Message.receiver_id == user1_id)
        ).order_by(Message.timestamp).all()
        
        return jsonify([{
            'id': msg.id,
            'content': msg.content,
            'sender_id': msg.sender_id,
            'receiver_id': msg.receiver_id,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages]), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500




# Logout endpoint
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

if __name__ == '__main__':
    # Ensure the app context is pushed for CLI operations
    with app.app_context():
        app.run(debug=True, host='0.0.0.0', port=5000)
