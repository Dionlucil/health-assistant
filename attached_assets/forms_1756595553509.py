from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField, SelectField, TextAreaField, IntegerField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from wtforms.widgets import CheckboxInput, ListWidget

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

class SymptomForm(FlaskForm):
    symptoms = MultiCheckboxField('Symptoms', 
                                choices=[
                                    ('fever', 'Fever'),
                                    ('headache', 'Headache'),
                                    ('cough', 'Cough'),
                                    ('sore_throat', 'Sore Throat'),
                                    ('fatigue', 'Fatigue'),
                                    ('nausea', 'Nausea'),
                                    ('vomiting', 'Vomiting'),
                                    ('diarrhea', 'Diarrhea'),
                                    ('abdominal_pain', 'Abdominal Pain'),
                                    ('chest_pain', 'Chest Pain'),
                                    ('shortness_of_breath', 'Shortness of Breath'),
                                    ('dizziness', 'Dizziness'),
                                    ('muscle_pain', 'Muscle Pain'),
                                    ('joint_pain', 'Joint Pain'),
                                    ('skin_rash', 'Skin Rash'),
                                    ('runny_nose', 'Runny Nose'),
                                    ('congestion', 'Congestion'),
                                    ('loss_of_appetite', 'Loss of Appetite'),
                                    ('difficulty_sleeping', 'Difficulty Sleeping'),
                                    ('weight_loss', 'Unexplained Weight Loss')
                                ],
                                validators=[DataRequired()])
    
    severity = RadioField('How severe are your symptoms?',
                         choices=[('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe')],
                         validators=[DataRequired()])
    
    duration = SelectField('How long have you had these symptoms?',
                          choices=[
                              ('hours', 'A few hours'),
                              ('1-2_days', '1-2 days'),
                              ('3-7_days', '3-7 days'),
                              ('1-2_weeks', '1-2 weeks'),
                              ('2-4_weeks', '2-4 weeks'),
                              ('more_than_month', 'More than a month')
                          ],
                          validators=[DataRequired()])
    
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, max=120)])
    gender = SelectField('Gender', 
                        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                        validators=[DataRequired()])
    
    additional_info = TextAreaField('Additional Information (Optional)',
                                   description='Please provide any additional details about your symptoms')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
