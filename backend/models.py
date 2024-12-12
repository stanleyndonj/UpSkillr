from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt

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

    # Relationships
    skills = db.relationship('Skill', backref='user', lazy=True)
    skill_requests = db.relationship('SkillRequest', backref='user', lazy=True)

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

    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Skill {self.name}>'

# SkillRequest model (Many-to-Many association with additional attribute)
class SkillRequest(db.Model):
    __tablename__ = 'skill_requests'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)

    # Relationships
    skill = db.relationship('Skill', backref='skill_requests')

    def __repr__(self):
        return f'<SkillRequest {self.description}>'

# Validators
@validates('email')
def validate_email(self, key, value):
    if '@' not in value:
        raise ValueError("Provided email is not valid.")
    return value
