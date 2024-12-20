from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy import Column, DateTime

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()

# User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    skills_offered = db.Column(db.Text, nullable=True)
    skills_requested = db.Column(db.Text, nullable=True)

    # Relationships
    skills = db.relationship('Skill', backref='skill_owner', lazy='dynamic', cascade='all, delete-orphan')
    skill_requests = db.relationship('SkillRequest', backref='request_user', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='reviewed_user', lazy='dynamic', cascade='all, delete-orphan')
    
    # Specify the foreign_keys argument to resolve ambiguity
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# Skill model
class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Relationship with SkillRequest
    skill_requests = db.relationship('SkillRequest', backref='skill', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Skill {self.name}>'

# SkillRequest model (Many-to-Many association with additional attribute)
class SkillRequest(db.Model):
    __tablename__ = 'skill_requests'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<SkillRequest {self.description}>'

# Review model
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Review {self.rating}>'

# Message model
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message from {self.sender_id} to {self.receiver_id}>'

# Validators
@validates('email')
def validate_email(self, key, value):
    if '@' not in value:
        raise ValueError("Provided email is not valid.")
    return value
