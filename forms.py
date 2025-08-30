from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from wtforms.fields import DateField

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    gender = SelectField('Gender', choices=[
        ('', 'Select Gender'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say')
    ], validators=[Optional()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])

class SymptomForm(FlaskForm):
    symptoms = SelectMultipleField('Symptoms', choices=[
        ('fever', 'Fever'),
        ('headache', 'Headache'),
        ('cough', 'Cough'),
        ('sore_throat', 'Sore Throat'),
        ('runny_nose', 'Runny Nose'),
        ('fatigue', 'Fatigue'),
        ('nausea', 'Nausea'),
        ('vomiting', 'Vomiting'),
        ('diarrhea', 'Diarrhea'),
        ('abdominal_pain', 'Abdominal Pain'),
        ('chest_pain', 'Chest Pain'),
        ('shortness_of_breath', 'Shortness of Breath'),
        ('dizziness', 'Dizziness'),
        ('muscle_aches', 'Muscle Aches'),
        ('joint_pain', 'Joint Pain'),
        ('skin_rash', 'Skin Rash'),
        ('loss_of_appetite', 'Loss of Appetite'),
        ('difficulty_sleeping', 'Difficulty Sleeping'),
        ('congestion', 'Congestion'),
        ('sneezing', 'Sneezing'),
        ('back_pain', 'Back Pain'),
        ('anxiety', 'Anxiety'),
        ('confusion', 'Confusion')
    ], validators=[DataRequired(message='Please select at least one symptom')])
    
    severity = SelectField('How severe are your symptoms?', choices=[
        ('mild', 'Mild - Noticeable but not interfering with daily activities'),
        ('moderate', 'Moderate - Somewhat interfering with daily activities'),
        ('severe', 'Severe - Significantly interfering with daily activities')
    ], validators=[DataRequired()])
    
    duration = SelectField('How long have you had these symptoms?', choices=[
        ('less_than_day', 'Less than a day'),
        ('1_3_days', '1-3 days'),
        ('4_7_days', '4-7 days'),
        ('1_2_weeks', '1-2 weeks'),
        ('2_4_weeks', '2-4 weeks'),
        ('more_than_month', 'More than a month')
    ], validators=[DataRequired()])
    
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=1, max=120)])
    gender = SelectField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], validators=[Optional()])
    
    additional_info = TextAreaField('Additional Information', validators=[Optional()], 
                                  description='Optional: Any additional details about your symptoms')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    gender = SelectField('Gender', choices=[
        ('', 'Select Gender'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say')
    ], validators=[Optional()])
