from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    consultations = db.relationship('Consultation', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)  # JSON string of symptoms
    severity = db.Column(db.String(20))
    duration = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    analysis_result = db.Column(db.Text)  # JSON string of analysis results
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Consultation {self.id} for User {self.user_id}>'

class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Symptom {self.name}>'
