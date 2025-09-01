from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import json
import uuid
from datetime import datetime
from forms import LoginForm, RegistrationForm

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_assistant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Simple User class for now
class User:
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
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def has_active_subscription(self):
        """Check if user has an active subscription"""
        if self.subscription_status == 'premium' and self.subscription_expires:
            return datetime.utcnow() < self.subscription_expires
        return False
    
    def can_use_free_consultation(self):
        """Check if user can still use free consultation"""
        return self.free_consultations_used < 1

# Simple file-based storage for users (persists between restarts)
import os
import pickle

USERS_FILE = 'users_data.pkl'

def load_users():
    """Load users from file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'rb') as f:
                data = pickle.load(f)
                users = data.get('users', {})
                counter = data.get('counter', 1)
                print(f"✅ Loaded {len(users)} users from file")
                return users, counter
        except Exception as e:
            print(f"⚠️ Error loading users: {e}")
            return {}, 1
    print("📝 No users file found, starting fresh")
    return {}, 1

def save_users(users_db, user_id_counter):
    """Save users to file"""
    try:
        data = {'users': users_db, 'counter': user_id_counter}
        with open(USERS_FILE, 'wb') as f:
            pickle.dump(data, f)
    except Exception as e:
        print(f"Warning: Could not save users data: {e}")

# Load existing users
users_db, user_id_counter = load_users()

def create_user(email, first_name, last_name, age, gender, password):
    global user_id_counter
    user = User(user_id_counter, email, first_name, last_name, age, gender)
    user.set_password(password)
    users_db[email] = user
    user_id_counter += 1
    save_users(users_db, user_id_counter)  # Save to file
    return user

def get_user_by_email(email):
    return users_db.get(email)

def get_user_by_id(user_id):
    for user in users_db.values():
        if user.id == user_id:
            return user
    return None

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")

# AI Doctor Chatbot Logic
class AIDoctor:
    def __init__(self):
        self.symptom_database = {
            'fever': {
                'diseases': ['Common Cold', 'Flu', 'COVID-19', 'Bacterial Infection'],
                'prescription': 'MEDICATIONS: Acetaminophen (Tylenol) 500-1000mg every 6-8 hours OR Ibuprofen (Advil) 200-400mg every 6-8 hours. Also: Rest, fluids, monitor temperature.',
                'severity': 'moderate'
            },
            'headache': {
                'diseases': ['Tension Headache', 'Migraine', 'Sinusitis', 'Dehydration'],
                'prescription': 'MEDICATIONS: Acetaminophen (Tylenol) 500-1000mg OR Ibuprofen (Advil) 200-400mg OR Aspirin 325-650mg. Also: Rest in quiet room, hydration.',
                'severity': 'mild'
            },
            'cough': {
                'diseases': ['Upper Respiratory Infection', 'Bronchitis', 'Allergies', 'Post-nasal drip'],
                'prescription': 'MEDICATIONS: Dextromethorphan (Robitussin DM) 15-30mg every 4-6 hours OR Guaifenesin (Mucinex) 200-400mg every 4 hours. Also: Honey, warm fluids, humidifier.',
                'severity': 'mild'
            },
            'fatigue': {
                'diseases': ['Stress', 'Anemia', 'Sleep disorder', 'Chronic fatigue'],
                'prescription': 'MEDICATIONS: Consider Vitamin B12 1000mcg daily OR Iron supplement if anemic. Also: Ensure 7-9 hours sleep, balanced diet, regular exercise.',
                'severity': 'mild'
            },
            'nausea': {
                'diseases': ['Gastritis', 'Food poisoning', 'Motion sickness', 'Anxiety'],
                'prescription': 'MEDICATIONS: Dimenhydrinate (Dramamine) 25-50mg every 4-6 hours OR Meclizine (Bonine) 25mg daily. Also: Small meals, ginger tea, avoid spicy foods.',
                'severity': 'moderate'
            },
            'chest_pain': {
                'diseases': ['Costochondritis', 'Muscle strain', 'Anxiety', 'Heart condition'],
                'prescription': 'MEDICATIONS: Ibuprofen (Advil) 200-400mg every 6-8 hours OR Naproxen (Aleve) 220mg every 8-12 hours. Also: Rest, avoid heavy lifting, warm compress.',
                'severity': 'moderate'
            },
            'sore_throat': {
                'diseases': ['Pharyngitis', 'Strep throat', 'Viral infection', 'Allergies'],
                'prescription': 'MEDICATIONS: Acetaminophen (Tylenol) 500-1000mg every 6-8 hours OR Ibuprofen (Advil) 200-400mg every 6-8 hours. Also: Warm salt water gargles, throat lozenges.',
                'severity': 'mild'
            },
            'runny_nose': {
                'diseases': ['Common Cold', 'Allergies', 'Sinusitis', 'Flu'],
                'prescription': 'MEDICATIONS: Pseudoephedrine (Sudafed) 30-60mg every 4-6 hours OR Loratadine (Claritin) 10mg daily for allergies. Also: Nasal saline spray, rest, fluids.',
                'severity': 'mild'
            },
            'muscle_aches': {
                'diseases': ['Viral infection', 'Overexertion', 'Flu', 'Stress'],
                'prescription': 'MEDICATIONS: Ibuprofen (Advil) 200-400mg every 6-8 hours OR Acetaminophen (Tylenol) 500-1000mg every 6-8 hours. Also: Rest, warm compress, gentle stretching.',
                'severity': 'mild'
            },
            'vaginal_discharge': {
                'diseases': ['Yeast infection', 'Bacterial vaginosis', 'STI', 'Hormonal changes'],
                'prescription': 'MEDICATIONS: For yeast infection: Clotrimazole (Gyne-Lotrimin) cream OR Fluconazole (Diflucan) 150mg single dose. Also: Maintain good hygiene, avoid douching, wear cotton underwear.',
                'severity': 'moderate'
            },
            'dizziness': {
                'diseases': ['Vertigo', 'Low blood pressure', 'Dehydration', 'Inner ear problems'],
                'prescription': 'MEDICATIONS: Meclizine (Bonine) 25mg daily for vertigo OR Dimenhydrinate (Dramamine) 25-50mg as needed. Also: Stay hydrated, avoid sudden movements, rest.',
                'severity': 'moderate'
            },
            'stomachache': {
                'diseases': ['Gastritis', 'Indigestion', 'Food poisoning', 'IBS'],
                'prescription': 'MEDICATIONS: Antacids (Tums, Rolaids) OR Famotidine (Pepcid) 20mg twice daily OR Omeprazole (Prilosec) 20mg daily. Also: Avoid spicy foods, eat small meals, stay hydrated.',
                'severity': 'mild'
            },
            'back_pain': {
                'diseases': ['Muscle strain', 'Herniated disc', 'Arthritis', 'Poor posture'],
                'prescription': 'MEDICATIONS: Ibuprofen (Advil) 200-400mg every 6-8 hours OR Naproxen (Aleve) 220mg every 8-12 hours. Also: Rest, ice/heat therapy, gentle stretching, proper posture.',
                'severity': 'moderate'
            },
            'diarrhea': {
                'diseases': ['Viral gastroenteritis', 'Food poisoning', 'IBS', 'Medication side effect'],
                'prescription': 'MEDICATIONS: Loperamide (Imodium) 2mg after each loose stool (max 8mg/day) OR Bismuth subsalicylate (Pepto-Bismol). Also: Stay hydrated, BRAT diet (bananas, rice, applesauce, toast).',
                'severity': 'moderate'
            }
        }
    
    def analyze_symptoms(self, symptoms_text):
        """Analyze symptoms and return diagnosis"""
        symptoms_text = symptoms_text.lower()
        matched_symptoms = []
        
        # Check for symptom keywords in the text (not just exact word matches)
        for symptom_key, symptom_data in self.symptom_database.items():
            if symptom_key in symptoms_text:
                matched_symptoms.append(symptom_key)
        
        # Also check for variations and related terms
        symptom_variations = {
            'headache': ['head', 'head ache', 'migraine', 'head pain', 'headache', 'headaches'],
            'cough': ['coughing', 'hack', 'hacking', 'cough', 'coughs'],
            'chest_pain': ['chest', 'chest pain', 'chest ache', 'rib pain', 'ribs', 'boob', 'breast pain', 'chest hurts', 'chest discomfort'],
            'fever': ['temperature', 'hot', 'burning up', 'fever', 'feverish'],
            'fatigue': ['tired', 'exhausted', 'weak', 'lethargic', 'fatigue', 'fatigued'],
            'nausea': ['sick', 'queasy', 'vomit', 'throwing up', 'nausea', 'nauseous'],
            'sore_throat': ['throat', 'sore throat', 'throat pain', 'throat hurts', 'throat ache'],
            'runny_nose': ['nose', 'runny nose', 'stuffy nose', 'nasal', 'congestion'],
            'muscle_aches': ['muscle', 'muscle pain', 'muscle ache', 'body ache', 'body pain', 'aching'],
            'vaginal_discharge': ['discharge', 'vaginal discharge', 'yeast infection', 'bacterial vaginosis', 'vaginal itching'],
            'dizziness': ['dizzy', 'dizziness', 'vertigo', 'lightheaded', 'lightheadedness', 'spinning'],
            'stomachache': ['stomach', 'stomach pain', 'stomach ache', 'stomachache', 'abdominal pain', 'belly pain', 'tummy pain'],
            'back_pain': ['back', 'back pain', 'back ache', 'lower back', 'upper back', 'spine pain'],
            'diarrhea': ['diarrhea', 'diarrhoea', 'loose stools', 'watery stools', 'bowel movement', 'stomach upset']
        }
        
        for symptom_key, variations in symptom_variations.items():
            if any(var in symptoms_text for var in variations):
                if symptom_key not in matched_symptoms:
                    matched_symptoms.append(symptom_key)
        
        if matched_symptoms:
            # Get the most severe symptom
            most_severe = max(matched_symptoms, key=lambda x: self.symptom_database[x]['severity'])
            diagnosis = self.symptom_database[most_severe]
            
            return {
                'disease': diagnosis['diseases'][0],
                'prescription': diagnosis['prescription'],
                'severity': diagnosis['severity'],
                'matched_symptoms': matched_symptoms
            }
        else:
            return {
                'disease': 'General Consultation Needed',
                'prescription': 'Please provide more specific symptoms or consult a healthcare provider.',
                'severity': 'unknown',
                'matched_symptoms': []
            }
    
    def get_response(self, user_message, chat_history=None, is_first_consultation=False):
        """Generate AI doctor response"""
        user_message = user_message.lower().strip()
        
        # Handle greetings - only on first interaction
        if any(word in user_message for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']) and not chat_history:
            return {
                'response': "Hello! How are you doing today? What symptoms are you experiencing?",
                'type': 'greeting',
                'requires_payment': False
            }
        
        # Handle symptom descriptions - check if any known symptoms are mentioned
        diagnosis = self.analyze_symptoms(user_message)
        
        # If we found symptoms, provide diagnosis and prescription
        if diagnosis['matched_symptoms']:
            symptoms_list = ', '.join(diagnosis['matched_symptoms']).replace('_', ' ')
            return {
                'response': f"I understand you're experiencing {symptoms_list}. Based on your symptoms, you may be experiencing **{diagnosis['disease']}**.\n\n**My Prescription:**\n{diagnosis['prescription']}\n\nWould you like me to explain the dosage or any side effects?\n\n**Important:** This is for informational purposes only and should not replace professional medical advice. If symptoms persist or worsen, please consult with a healthcare provider.",
                'type': 'diagnosis',
                'diagnosis': diagnosis,
                'requires_payment': True
            }
        
        # Check for general symptom indicators
        if any(word in user_message for word in ['symptom', 'feel', 'pain', 'hurt', 'sick', 'unwell', 'ache', 'sore', 'discharge', 'dizzy', 'stomach', 'nauseous']):
            return {
                'response': f"I can see you're not feeling well. Based on what you've described, you may be experiencing **{diagnosis['disease']}**.\n\n**My Prescription:**\n{diagnosis['prescription']}\n\nWould you like me to explain the dosage or any side effects?\n\n**Important:** This is for informational purposes only and should not replace professional medical advice. If symptoms persist or worsen, please consult with a healthcare provider.",
                'type': 'diagnosis',
                'diagnosis': diagnosis,
                'requires_payment': True
            }
        
        # Handle follow-up questions about dosage/side effects
        if any(word in user_message for word in ['dosage', 'how much', 'how often', 'side effect', 'side effects', 'explain']):
            return {
                'response': "I'd be happy to explain the dosage and potential side effects. Please let me know which specific medication you'd like me to explain in detail.",
                'type': 'clarification',
                'requires_payment': False
            }
        
        # Handle thank you messages
        if any(word in user_message for word in ['thank', 'thanks', 'appreciate', 'helpful']):
            return {
                'response': "You're very welcome! I'm glad I could help. Remember to monitor your symptoms and don't hesitate to seek professional medical care if needed. Take care! 👨‍⚕️",
                'type': 'gratitude',
                'requires_payment': False
            }
        
        # Handle questions about medications
        if any(word in user_message for word in ['medication', 'medicine', 'drug', 'pill']):
            return {
                'response': "I can provide general information about medications, but please remember that I cannot give specific medical advice. Always consult with a healthcare provider or pharmacist before taking any medications, especially if you have other medical conditions or are taking other medications.\n\nIs there a specific medication you'd like to know more about?",
                'type': 'medication_info',
                'requires_payment': False
            }
        
        # Handle general conversation
        if any(word in user_message for word in ['how are you', 'how do you do', 'nice to meet', 'good to see']):
            return {
                'response': "I'm doing well, thank you for asking! I'm here to help you with any health concerns. What symptoms are you experiencing today?",
                'type': 'conversation',
                'requires_payment': False
            }
        
        # Default response - more empathetic and direct
        return {
            'response': "I understand you're concerned about your health. Please describe your symptoms so I can help you better. For example, are you experiencing any pain, fever, nausea, or other discomfort?",
            'type': 'general',
            'requires_payment': False
        }

# Initialize AI Doctor
ai_doctor = AIDoctor()

# Add custom Jinja2 filter for JSON parsing
@app.template_filter('from_json')
def from_json_filter(value):
    import json
    try:
        return json.loads(value) if value else []
    except (json.JSONDecodeError, TypeError):
        return []

# Simple route for testing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return "Health Assistant is working!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        print(f"🔍 Login attempt for: {email}")
        print(f"📊 Total users in database: {len(users_db)}")
        
        user = get_user_by_email(email)
        
        if user:
            print(f"✅ User found: {user.email}")
            if user.check_password(password):
                login_user(user, remember=True)
                flash('Login successful!', 'success')
                print(f"🎉 Login successful for: {email}")
                return redirect(url_for('dashboard'))
            else:
                flash('Login failed. Invalid password.', 'danger')
                print(f"❌ Invalid password for: {email}")
        else:
            flash('Login failed. User not found.', 'danger')
            print(f"❌ User not found: {email}")
        
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        password = request.form.get('password')
        
        if get_user_by_email(email):
            flash('Email already in use. Please choose a different one.', 'warning')
            return redirect(url_for('register'))
        
        # Check password confirmation
        password2 = request.form.get('password2')
        if password != password2:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        
        try:
            age = int(age)
            user = create_user(email, first_name, last_name, age, gender, password)
            
            # Login the user and remember them
            login_user(user, remember=True)
            
            flash('Registration successful! You are now logged in.', 'success')
            return redirect(url_for('dashboard'))
        except ValueError:
            flash('Age must be a number.', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/symptoms')
def symptoms():
    if not current_user.is_authenticated:
        flash('Please login to access the symptom checker.', 'warning')
        return redirect(url_for('login'))
    
    # Check if user needs to pay
    if current_user.free_consultations_used >= 1:
        flash('You have used your free consultation. Please upgrade to continue using our services.', 'info')
        return redirect(url_for('pricing'))
    
    return render_template('symptoms.html')

@app.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        flash('Please login to access your dashboard.', 'warning')
        return redirect(url_for('login'))
    
    # Mock data for dashboard (in a real app, this would come from database)
    recent_consultations = []  # Empty for now
    total_consultations = 0
    payment_info = {
        'payment_required': current_user.free_consultations_used >= 1
    }
    
    return render_template('dashboard.html', 
                         recent_consultations=recent_consultations,
                         total_consultations=total_consultations,
                         payment_info=payment_info)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/ai_doctor')
def ai_doctor_page():
    if not current_user.is_authenticated:
        flash('Please login to access the AI Doctor.', 'warning')
        return redirect(url_for('login'))
    
    # Check if user needs to pay
    if current_user.free_consultations_used >= 1:
        flash('You have used your free consultation. Please upgrade to continue using our services.', 'info')
        return redirect(url_for('pricing'))
    
    return render_template('ai_doctor.html')

@app.route('/ai_doctor/chat', methods=['POST'])
def ai_doctor_chat():
    """Handle AI Doctor chat requests"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Please log in to use AI Doctor'}), 401
    
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get AI response
    ai_response = ai_doctor.get_response(user_message)
    
    # Check if this response requires payment (diagnosis/prescription)
    if ai_response.get('requires_payment', False):
        # Check if user has used their free consultation
        if not current_user.can_use_free_consultation() and not current_user.has_active_subscription():
            return jsonify({
                'error': 'You have used your free consultation. Please complete payment to proceed with your treatment.',
                'redirect': url_for('pricing'),
                'payment_required': True
            }), 402
        
        # If this is a diagnosis (prescription), mark free consultation as used
        if current_user.can_use_free_consultation():
            current_user.free_consultations_used += 1
            save_users(users_db, user_id_counter)  # Save the updated user data
            print(f"🎯 User {current_user.email} used their free consultation")
    
    # Save to session for history (in a real app, this would go to database)
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    session['chat_history'].append({
        'user': user_message,
        'ai': ai_response['response'],
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify({
        'response': ai_response['response'],
        'type': ai_response['type'],
        'diagnosis': ai_response.get('diagnosis', None),
        'payment_required': False
    })

@app.route('/ai_doctor/history')
def ai_doctor_history():
    """Get chat history"""
    return jsonify(session.get('chat_history', []))

@app.route('/history')
def history_list():
    """View consultation history"""
    if not current_user.is_authenticated:
        flash('Please login to view your consultation history.', 'warning')
        return redirect(url_for('login'))
    
    # Mock data for now - in a real app, this would come from database
    consultations = []
    
    return render_template('history.html', consultations=consultations)

@app.route('/results/<int:consultation_id>')
def results(consultation_id):
    """View consultation results"""
    if not current_user.is_authenticated:
        flash('Please login to view consultation results.', 'warning')
        return redirect(url_for('login'))
    
    # Mock data for now - in a real app, this would come from database
    consultation = {
        'id': consultation_id,
        'symptoms': ['fever', 'headache'],
        'diagnosis': 'Common Cold',
        'prescription': 'Rest, fluids, acetaminophen for fever',
        'created_at': datetime.utcnow(),
        'severity': 'mild'
    }
    
    return render_template('results.html', consultation=consultation)

@app.route('/profile')
def profile():
    if not current_user.is_authenticated:
        flash('Please login to access your profile.', 'warning')
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("=" * 60)
    print("🏥 Community Health Assistant")
    print("=" * 60)
    print("Starting server...")
    print("Visit: http://localhost:5000")
    print("=" * 60)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
