from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# This will be a simple User class for now
class User(UserMixin):
    def __init__(self, id, email, first_name, last_name, age, gender):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.password_hash = None
        self.created_at = datetime.utcnow()
        self.last_login = None
        self.free_consultations_used = 0
        self.subscription_status = 'free'
        self.subscription_expires = None
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def can_use_free_consultation(self):
        return self.free_consultations_used < 1
    
    def has_active_subscription(self):
        if self.subscription_status == 'premium':
            return self.subscription_expires and self.subscription_expires > datetime.utcnow()
        return False
    
    def needs_payment(self):
        return not self.can_use_free_consultation() and not self.has_active_subscription()
    
    def __repr__(self):
        return f'<User {self.email}>'

# Simple in-memory storage for users (in a real app, this would be a database)
users_db = {}
user_id_counter = 1

def create_user(email, first_name, last_name, age, gender, password):
    global user_id_counter
    user = User(user_id_counter, email, first_name, last_name, age, gender)
    user.set_password(password)
    users_db[email] = user
    user_id_counter += 1
    return user

def get_user_by_email(email):
    return users_db.get(email)

def get_user_by_id(user_id):
    for user in users_db.values():
        if user.id == user_id:
            return user
    return None

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)  # JSON string of symptoms
    severity = db.Column(db.String(20))
    duration = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    additional_info = db.Column(db.Text)
    analysis = db.Column(db.Text)  # JSON string of analysis results
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    payment_required = db.Column(db.Boolean, default=False)
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, free
    
    def __repr__(self):
        return f'<Consultation {self.id} for User {self.user_id}>'

class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Symptom {self.name}>'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    payment_type = db.Column(db.String(20))  # consultation, subscription
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    transaction_id = db.Column(db.String(100), unique=True)
    consultation_id = db.Column(db.Integer, db.ForeignKey('consultation.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Payment {self.id} for User {self.user_id}>'

class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ChatSession {self.session_id} for User {self.user_id}>'

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), db.ForeignKey('chat_session.session_id'), nullable=False)
    message_type = db.Column(db.String(10), nullable=False)  # user, ai
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatMessage {self.id} in Session {self.session_id}>'

class PricingPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    consultations_limit = db.Column(db.Integer, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    features = db.Column(db.Text)  # JSON string of features
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PricingPlan {self.name}>'
