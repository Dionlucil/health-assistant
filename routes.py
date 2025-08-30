import json
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Consultation
from forms import LoginForm, RegisterForm, SymptomForm, ProfileForm
from symptom_analyzer import SymptomAnalyzer

# Initialize symptom analyzer
analyzer = SymptomAnalyzer()

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
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email address already registered.', 'danger')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User()
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.date_of_birth = form.date_of_birth.data
        user.gender = form.gender.data
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    recent_consultations = Consultation.query.filter_by(user_id=current_user.id)\
                                           .order_by(Consultation.created_at.desc())\
                                           .limit(5).all()
    
    total_consultations = Consultation.query.filter_by(user_id=current_user.id).count()
    
    return render_template('dashboard.html', 
                         recent_consultations=recent_consultations,
                         total_consultations=total_consultations)

@app.route('/symptoms', methods=['GET', 'POST'])
@login_required
def symptoms():
    form = SymptomForm()
    
    if form.validate_on_submit():
        try:
            # Analyze symptoms
            symptoms_list = form.symptoms.data or []
            age_value = form.age.data or current_user.date_of_birth.year if current_user.date_of_birth else 25
            analysis_result = analyzer.analyze_symptoms(
                symptoms=symptoms_list,
                age=age_value,
                gender=form.gender.data or current_user.gender or 'other',
                severity=form.severity.data or 'mild'
            )
            
            # Save consultation to database
            consultation = Consultation(
                user_id=current_user.id,
                symptoms=json.dumps(symptoms_list),
                severity=form.severity.data,
                duration=form.duration.data,
                age=form.age.data,
                gender=form.gender.data,
                additional_info=form.additional_info.data,
                analysis_result=json.dumps(analysis_result)
            )
            
            db.session.add(consultation)
            db.session.commit()
            
            # Store consultation ID in session for results page
            session['consultation_id'] = consultation.id
            
            return redirect(url_for('results'))
            
        except Exception as e:
            flash('Error processing your symptoms. Please try again.', 'danger')
            return render_template('symptoms.html', form=form)
    
    return render_template('symptoms.html', form=form)

@app.route('/results')
@login_required
def results():
    consultation_id = session.get('consultation_id')
    if not consultation_id:
        flash('No consultation data found.', 'warning')
        return redirect(url_for('symptoms'))
    
    consultation = Consultation.query.get_or_404(consultation_id)
    
    # Ensure user can only view their own consultations
    if consultation.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Parse stored data
    symptoms = json.loads(consultation.symptoms)
    analysis_result = json.loads(consultation.analysis_result)
    
    return render_template('results.html', 
                         consultation=consultation,
                         symptoms=symptoms,
                         analysis_result=analysis_result)

@app.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    consultations = Consultation.query.filter_by(user_id=current_user.id)\
                                    .order_by(Consultation.created_at.desc())\
                                    .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('history.html', consultations=consultations)

@app.route('/history/<int:consultation_id>')
@login_required
def view_consultation(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    
    # Ensure user can only view their own consultations
    if consultation.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('history'))
    
    # Parse stored data
    symptoms = json.loads(consultation.symptoms)
    analysis_result = json.loads(consultation.analysis_result)
    
    return render_template('results.html', 
                         consultation=consultation,
                         symptoms=symptoms,
                         analysis_result=analysis_result)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        try:
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.date_of_birth = form.date_of_birth.data
            current_user.gender = form.gender.data
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile. Please try again.', 'danger')
    
    return render_template('profile.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
