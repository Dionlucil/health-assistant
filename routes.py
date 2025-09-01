import os
import uuid
import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Consultation, Symptom, ChatSession, ChatMessage
from .forms import LoginForm, RegistrationForm, SymptomForm
from .symptom_analyzer import SymptomAnalyzer

# Import services
from ai_doctor import AIDoctor
from payment_service import PaymentService

# Initialize services
def get_ai_doctor():
    """Get AI doctor instance with error handling"""
    try:
        return AIDoctor()
    except Exception as e:
        print(f"Error creating AI doctor: {e}")
        return None

def get_payment_service():
    """Get payment service instance with error handling"""
    try:
        return PaymentService()
    except Exception as e:
        print(f"Error creating payment service: {e}")
        return None

# Initialize services
ai_doctor = get_ai_doctor()
payment_service = get_payment_service()

# Global variable to track AI doctor status
_ai_doctor_available = ai_doctor is not None

def get_safe_ai_doctor():
    """Safely get AI doctor instance, recreating if necessary"""
    global ai_doctor, _ai_doctor_available
    
    if ai_doctor is None or not hasattr(ai_doctor, 'get_medical_response'):
        try:
            ai_doctor = get_ai_doctor()
            _ai_doctor_available = ai_doctor is not None
        except Exception as e:
            print(f"Error recreating AI doctor: {e}")
            ai_doctor = None
            _ai_doctor_available = False
    
    return ai_doctor

# Initialize symptom analyzer
symptom_analyzer = SymptomAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('dashboard')
            return redirect(next_page)
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please login.', 'error')
            return redirect(url_for('login'))
        
        # Create new user
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            age=form.age.data,
            gender=form.gender.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's consultations
    consultations = Consultation.query.filter_by(user_id=current_user.id).order_by(Consultation.created_at.desc()).all()
    
    # Calculate payment info if payment service is available
    payment_info = None
    if payment_service:
        payment_info = payment_service.calculate_consultation_cost(current_user)
    
    return render_template('dashboard.html', 
                         recent_consultations=consultations, 
                         payment_info=payment_info)

@app.route('/symptoms', methods=['GET', 'POST'])
@login_required
def symptoms():
    form = SymptomForm()
    
    if form.validate_on_submit():
        # Convert symptoms list to string for storage and analysis
        symptoms_list = form.symptoms.data if form.symptoms.data else []
        symptoms_text = ', '.join(symptoms_list) if symptoms_list else []
        
        # Check if payment is required
        payment_required = False
        if payment_service and payment_service.enabled:
            try:
                payment_info = payment_service.calculate_consultation_cost(current_user)
                payment_required = payment_info.get('payment_required', False)
                
                if payment_required:
                    # Create consultation with payment required
                    consultation = Consultation(
                        user_id=current_user.id,
                        symptoms=symptoms_text,
                        age=current_user.age,
                        gender=current_user.gender,
                        payment_required=True,
                        payment_status='pending'
                    )
                    db.session.add(consultation)
                    db.session.commit()
                    
                    # Create payment intent
                    payment_result = payment_service.create_payment_intent(
                        amount=payment_info['cost'],
                        payment_type='consultation',
                        user_id=current_user.id,
                        consultation_id=consultation.id
                    )
                    
                    if payment_result.get('success', True):
                        session['payment_intent'] = payment_result
                        return redirect(url_for('payment'))
                    else:
                        flash('Payment setup failed. Please try again.', 'error')
                        return redirect(url_for('symptoms'))
            except Exception as e:
                print(f"Payment service error: {e}")
                # Fall back to free consultation if payment service fails
                payment_required = False
        
        # If payment is not required or payment service is not available, create free consultation
        if payment_required:
            current_user.free_consultations_used += 1
        
        consultation = Consultation(
            user_id=current_user.id,
            symptoms=symptoms_text,
            age=current_user.age,
            gender=current_user.gender,
            payment_required=False,
            payment_status='free'
        )
        
        db.session.add(consultation)
        db.session.commit()
        
        # Analyze symptoms - pass the symptoms list to the analyzer
        analysis = symptom_analyzer.analyze_symptoms(symptoms_list, current_user.age, current_user.gender, form.severity.data)
        consultation.analysis = json.dumps(analysis)  # Convert dictionary to JSON string
        db.session.commit()
        
        return redirect(url_for('results', consultation_id=consultation.id))
    
    return render_template('symptoms.html', form=form)

@app.route('/results/<int:consultation_id>')
@login_required
def results(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    
    # Check if user owns this consultation
    if consultation.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    # Check payment status for paid consultations
    if consultation.payment_required and consultation.payment_status != 'paid':
        flash('Payment required to view results.', 'error')
        return redirect(url_for('dashboard'))
    
    # Parse analysis JSON and prepare data for template
    analysis_result = {}
    symptoms = []
    
    if consultation.analysis:
        try:
            analysis_result = json.loads(consultation.analysis)
        except (json.JSONDecodeError, TypeError):
            analysis_result = {
                'disclaimer': 'Analysis data could not be loaded.',
                'urgency': 'low',
                'conditions': [],
                'advice': ['Please consult a healthcare professional for proper diagnosis.']
            }
    
    # Extract symptoms from consultation.symptoms
    if consultation.symptoms:
        symptoms = [s.strip() for s in consultation.symptoms.split(',') if s.strip()]
    
    return render_template('results.html', 
                         consultation=consultation,
                         analysis_result=analysis_result,
                         symptoms=symptoms)

@app.route('/history')
@login_required
def history_list():
    # Get all consultations for the current user
    consultations = Consultation.query.filter_by(user_id=current_user.id).order_by(Consultation.created_at.desc()).all()
    return render_template('history_list.html', consultations=consultations)

@app.route('/history/<int:consultation_id>')
@login_required
def history(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    
    # Check if user owns this consultation
    if consultation.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    # Check payment status for paid consultations
    if consultation.payment_required and consultation.payment_status != 'paid':
        flash('Payment required to view results.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('history.html', consultation=consultation)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# AI Doctor routes
@app.route('/ai-doctor')
@login_required
def ai_doctor():
    if payment_service:
        payment_info = payment_service.calculate_consultation_cost(current_user)
    else:
        payment_info = {'payment_required': False, 'cost': 0.0}
    
    return render_template('ai_doctor.html', payment_info=payment_info)

@app.route('/ai-doctor/start-chat', methods=['POST'])
@login_required
def start_chat():
    # Check payment status
    if payment_service:
        payment_info = payment_service.calculate_consultation_cost(current_user)
        if payment_info['payment_required']:
            return jsonify({'success': False, 'payment_required': True, 'message': 'Payment required'})
    
    # Create chat session
    session_id = str(uuid.uuid4())
    chat_session = ChatSession(
        user_id=current_user.id,
        session_id=session_id,
        is_active=True
    )
    db.session.add(chat_session)
    
    # Add welcome message
    welcome_message = ChatMessage(
        session_id=session_id,
        message_type='ai',
        content="Hello! I'm Dr. Sarah Chen, your AI medical assistant. How can I help you today? Please describe your symptoms or ask any health-related questions."
    )
    db.session.add(welcome_message)
    db.session.commit()
    
    return jsonify({'success': True, 'session_id': session_id})

@app.route('/ai-doctor/send-message', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    message = data.get('message', '').strip()
    session_id = data.get('session_id')
    
    if not message or not session_id:
        return jsonify({'success': False, 'message': 'Invalid request'})
    
    # Save user message
    user_message = ChatMessage(
        session_id=session_id,
        message_type='user',
        content=message
    )
    db.session.add(user_message)
    
    # Get chat history
    chat_history = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
    history_data = [
        {'type': msg.message_type, 'content': msg.content}
        for msg in chat_history
    ]
    
    # Get AI response with error handling
    safe_ai_doctor = get_safe_ai_doctor()
    
    if not safe_ai_doctor:
        return jsonify({
            'success': False,
            'error': 'AI doctor service is temporarily unavailable. Please try again.'
        }), 500
    
    try:
        ai_response = safe_ai_doctor.get_medical_response(message, history_data)
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return jsonify({
            'success': False,
            'error': 'Sorry, I encountered an error. Please try again.'
        }), 500
    
    # Save AI response
    ai_message = ChatMessage(
        session_id=session_id,
        message_type='ai',
        content=ai_response['response']
    )
    db.session.add(ai_message)
    
    # Update session activity
    chat_session = ChatSession.query.filter_by(session_id=session_id).first()
    if chat_session:
        chat_session.last_activity = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'ai_response': ai_response['response'],
        'medications': ai_response.get('medications', []),
        'advice': ai_response.get('advice', [])
    })

@app.route('/ai-doctor/get-history/<session_id>')
@login_required
def get_chat_history(session_id):
    messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
    return jsonify({
        'success': True,
        'messages': [
            {
                'type': msg.message_type,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat()
            }
            for msg in messages
        ]
    })

@app.route('/ai-doctor/status')
@login_required
def ai_doctor_status():
    """Check AI doctor service status"""
    safe_ai_doctor = get_safe_ai_doctor()
    return jsonify({
        'success': True,
        'available': safe_ai_doctor is not None,
        'has_methods': hasattr(safe_ai_doctor, 'get_medical_response') if safe_ai_doctor else False,
        'type': str(type(safe_ai_doctor)) if safe_ai_doctor else 'None'
    })

# Payment routes
@app.route('/payment')
@login_required
def payment():
    if not payment_service:
        flash('Payment service not available.', 'error')
        return redirect(url_for('dashboard'))
    
    payment_intent = session.get('payment_intent')
    if not payment_intent:
        flash('No payment information found.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('payment.html', payment_intent=payment_intent)

@app.route('/payment/success')
@login_required
def payment_success():
    if not payment_service:
        flash('Payment service not available.', 'error')
        return redirect(url_for('dashboard'))
    
    payment_intent_id = request.args.get('payment_intent')
    if not payment_intent_id:
        flash('Payment information not found.', 'error')
        return redirect(url_for('dashboard'))
    
    # Process payment success
    result = payment_service.process_payment_success(payment_intent_id)
    
    if result['success']:
        # Trigger AI analysis for the consultation
        consultation_id = result.get('consultation_id')
        if consultation_id:
            consultation = Consultation.query.get(consultation_id)
            if consultation:
                safe_ai_doctor = get_safe_ai_doctor()
                if safe_ai_doctor:
                    try:
                        # Analyze symptoms with AI
                        analysis = safe_ai_doctor.analyze_symptoms_for_prescription(
                            consultation.symptoms.split(','),
                            consultation.age,
                            consultation.gender
                        )
                        consultation.analysis = json.dumps(analysis)  # Convert dictionary to JSON string
                        db.session.commit()
                    except Exception as e:
                        print(f"Error in AI analysis: {e}")
                        # Continue without AI analysis
                        db.session.commit()
                else:
                    # Save basic consultation without AI analysis
                    db.session.commit()
        
        flash('Payment successful! Your consultation results are ready.', 'success')
        return redirect(url_for('results', consultation_id=consultation_id))
    else:
        flash('Payment processing failed. Please contact support.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/pricing')
def pricing():
    if payment_service:
        plans = payment_service.get_pricing_plans()
    else:
        plans = {}
    return render_template('pricing.html', plans=plans)

@app.route('/subscribe/<plan_name>')
@login_required
def subscribe(plan_name):
    if not payment_service:
        flash('Payment service not available.', 'error')
        return redirect(url_for('dashboard'))
    
    # Create subscription payment
    payment_result = payment_service.create_subscription_payment(current_user.id, plan_name)
    
    if payment_result.get('success', True):
        session['payment_intent'] = payment_result
        return redirect(url_for('payment'))
    else:
        flash('Failed to create subscription payment.', 'error')
        return redirect(url_for('pricing'))
