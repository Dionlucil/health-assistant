import random
from datetime import datetime

class SymptomAnalyzer:
    def __init__(self):
        # Define common medical conditions and their associated symptoms
        self.conditions_database = {
            'common_cold': {
                'name': 'Common Cold',
                'symptoms': ['runny_nose', 'sneezing', 'sore_throat', 'cough', 'congestion', 'mild_fever'],
                'description': 'A viral infection of the upper respiratory tract that is generally harmless.',
                'urgency': 'low',
                'advice': [
                    'Get plenty of rest and stay hydrated',
                    'Use over-the-counter pain relievers if needed',
                    'Try warm salt water gargling for sore throat',
                    'Consider using a humidifier'
                ]
            },
            'influenza': {
                'name': 'Influenza (Flu)',
                'symptoms': ['fever', 'fatigue', 'muscle_aches', 'headache', 'cough', 'sore_throat'],
                'description': 'A viral infection that attacks the respiratory system with more severe symptoms than a cold.',
                'urgency': 'medium',
                'advice': [
                    'Rest and stay well-hydrated',
                    'Consider antiviral medication if within 48 hours of symptom onset',
                    'Monitor fever and seek care if it persists',
                    'Avoid contact with others to prevent spread'
                ]
            },
            'gastroenteritis': {
                'name': 'Gastroenteritis',
                'symptoms': ['nausea', 'vomiting', 'diarrhea', 'abdominal_pain', 'fever', 'fatigue'],
                'description': 'Inflammation of the stomach and intestines, often called stomach flu.',
                'urgency': 'medium',
                'advice': [
                    'Stay hydrated with clear fluids',
                    'Follow the BRAT diet (bananas, rice, applesauce, toast)',
                    'Avoid dairy and fatty foods temporarily',
                    'Seek care if symptoms worsen or persist'
                ]
            },
            'migraine': {
                'name': 'Migraine Headache',
                'symptoms': ['headache', 'nausea', 'dizziness', 'sensitivity_to_light'],
                'description': 'A type of headache that can cause severe throbbing pain, usually on one side of the head.',
                'urgency': 'medium',
                'advice': [
                    'Rest in a quiet, dark room',
                    'Apply cold or warm compress to head or neck',
                    'Stay hydrated and maintain regular sleep schedule',
                    'Consider over-the-counter pain relievers'
                ]
            },
            'anxiety_disorder': {
                'name': 'Anxiety',
                'symptoms': ['anxiety', 'difficulty_sleeping', 'fatigue', 'muscle_tension', 'headache'],
                'description': 'A mental health condition characterized by excessive worry and physical symptoms.',
                'urgency': 'medium',
                'advice': [
                    'Practice deep breathing and relaxation techniques',
                    'Maintain regular exercise and sleep schedule',
                    'Limit caffeine and alcohol intake',
                    'Consider speaking with a mental health professional'
                ]
            },
            'respiratory_infection': {
                'name': 'Respiratory Infection',
                'symptoms': ['cough', 'shortness_of_breath', 'chest_pain', 'fever', 'fatigue'],
                'description': 'An infection affecting the respiratory system that may require medical attention.',
                'urgency': 'high',
                'advice': [
                    'Seek medical attention promptly',
                    'Monitor breathing difficulty',
                    'Rest and stay hydrated',
                    'Avoid strenuous activities'
                ]
            }
        }
    
    def analyze_symptoms(self, symptoms, age=30, gender='other', severity='mild'):
        """
        Analyze symptoms and return possible conditions with recommendations
        """
        if not symptoms:
            return self._get_default_response()
        
        # Calculate condition probabilities
        condition_scores = {}
        
        for condition_id, condition_data in self.conditions_database.items():
            score = self._calculate_condition_probability(symptoms, condition_data['symptoms'])
            if score > 0:
                condition_scores[condition_id] = score
        
        # Sort conditions by probability
        sorted_conditions = sorted(condition_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Generate response
        response = {
            'disclaimer': 'This assessment is for informational purposes only and does not constitute medical advice. Please consult with a healthcare professional for proper diagnosis and treatment.',
            'urgency': self._determine_urgency(symptoms, severity),
            'conditions': [],
            'advice': []
        }
        
        # Add top matching conditions
        for condition_id, probability in sorted_conditions[:3]:
            condition = self.conditions_database[condition_id].copy()
            condition['probability'] = probability
            condition['common_symptoms'] = [s for s in symptoms if s in condition['symptoms']]
            response['conditions'].append(condition)
        
        # Generate general advice
        response['advice'] = self._generate_advice(symptoms, severity, age)
        
        return response
    
    def _calculate_condition_probability(self, user_symptoms, condition_symptoms):
        """Calculate how well user symptoms match a condition"""
        if not user_symptoms or not condition_symptoms:
            return 0
        
        matching_symptoms = set(user_symptoms) & set(condition_symptoms)
        total_condition_symptoms = len(condition_symptoms)
        
        if total_condition_symptoms == 0:
            return 0
        
        # Base probability on percentage of condition symptoms that match
        base_probability = len(matching_symptoms) / total_condition_symptoms
        
        # Bonus for having many matching symptoms
        if len(matching_symptoms) >= 3:
            base_probability += 0.1
        
        return min(base_probability, 1.0)
    
    def _determine_urgency(self, symptoms, severity):
        """Determine urgency level based on symptoms and severity"""
        high_urgency_symptoms = [
            'chest_pain', 'shortness_of_breath', 'difficulty_breathing',
            'severe_abdominal_pain', 'confusion', 'severe_headache'
        ]
        
        medium_urgency_symptoms = [
            'fever', 'persistent_vomiting', 'severe_pain', 'dizziness'
        ]
        
        # Check for high urgency symptoms
        if any(symptom in high_urgency_symptoms for symptom in symptoms):
            return 'high'
        
        # Check severity level
        if severity == 'severe':
            return 'high'
        elif severity == 'moderate':
            return 'medium'
        
        # Check for medium urgency symptoms
        if any(symptom in medium_urgency_symptoms for symptom in symptoms):
            return 'medium'
        
        return 'low'
    
    def _generate_advice(self, symptoms, severity, age):
        """Generate personalized health advice"""
        advice = []
        
        # Basic care advice
        advice.append('Monitor your symptoms and note any changes')
        advice.append('Stay well-hydrated by drinking plenty of fluids')
        advice.append('Get adequate rest to help your body recover')
        
        # Symptom-specific advice
        if 'fever' in symptoms:
            advice.append('Monitor your temperature and consider fever reducers if needed')
        
        if 'cough' in symptoms:
            advice.append('Use a humidifier or breathe steam to soothe your throat')
        
        if 'headache' in symptoms:
            advice.append('Try resting in a quiet, dark room')
        
        if 'nausea' in symptoms or 'vomiting' in symptoms:
            advice.append('Eat small, frequent meals and avoid greasy foods')
        
        # Age-specific advice
        if age >= 65:
            advice.append('Consider contacting your healthcare provider due to increased risk factors')
        elif age <= 18:
            advice.append('Ensure proper supervision and consider pediatric-specific care')
        
        # Severity-specific advice
        if severity == 'severe':
            advice.append('Consider seeking medical attention due to symptom severity')
        
        return advice
    
    def _get_default_response(self):
        """Return default response when no symptoms are provided"""
        return {
            'disclaimer': 'This assessment is for informational purposes only and does not constitute medical advice. Please consult with a healthcare professional for proper diagnosis and treatment.',
            'urgency': 'low',
            'conditions': [],
            'advice': [
                'If you are experiencing symptoms, please select them for a proper assessment',
                'Maintain a healthy lifestyle with regular exercise and balanced nutrition',
                'Schedule regular check-ups with your healthcare provider',
                'Seek immediate medical attention for any emergency symptoms'
            ]
        }
