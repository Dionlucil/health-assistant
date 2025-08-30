import os
import json
import requests
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class SymptomAnalyzer:
    def __init__(self):
        self.api_key = os.environ.get("MEDICAL_API_KEY", "demo_key")
        self.base_url = "https://api.infermedica.com/v3"
        
    def analyze_symptoms(self, symptoms: List[str], age: int, gender: str, severity: str = "moderate") -> Dict[str, Any]:
        """
        Analyze symptoms and return possible conditions with advice.
        This is a simplified implementation that would use a real medical API in production.
        """
        try:
            # In a real implementation, this would call an actual medical API like Infermedica
            # For now, we'll provide a structured response based on common symptom patterns
            
            analysis_result = {
                "conditions": self._get_possible_conditions(symptoms, age, gender),
                "advice": self._get_general_advice(symptoms, severity),
                "urgency": self._assess_urgency(symptoms, severity),
                "disclaimer": "This analysis is for informational purposes only and should not replace professional medical advice. Please consult with a healthcare provider for proper diagnosis and treatment.",
                "timestamp": "2024-01-01T00:00:00Z"
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing symptoms: {str(e)}")
            return {
                "error": "Unable to analyze symptoms at this time. Please try again later.",
                "conditions": [],
                "advice": ["Please consult with a healthcare provider."],
                "urgency": "unknown",
                "disclaimer": "This analysis is for informational purposes only and should not replace professional medical advice."
            }
    
    def _get_possible_conditions(self, symptoms: List[str], age: int, gender: str) -> List[Dict[str, Any]]:
        """Get possible conditions based on symptoms."""
        conditions = []
        
        # Common cold/flu pattern
        if any(symptom in symptoms for symptom in ['fever', 'cough', 'sore_throat', 'runny_nose', 'congestion']):
            conditions.append({
                "name": "Common Cold or Flu",
                "probability": 0.75,
                "description": "Viral infection affecting the upper respiratory system",
                "common_symptoms": ["fever", "cough", "sore_throat", "runny_nose", "fatigue"]
            })
        
        # Gastrointestinal issues
        if any(symptom in symptoms for symptom in ['nausea', 'vomiting', 'diarrhea', 'abdominal_pain']):
            conditions.append({
                "name": "Gastroenteritis",
                "probability": 0.65,
                "description": "Inflammation of the stomach and intestines",
                "common_symptoms": ["nausea", "vomiting", "diarrhea", "abdominal_pain", "fever"]
            })
        
        # Respiratory issues
        if any(symptom in symptoms for symptom in ['shortness_of_breath', 'chest_pain', 'cough']):
            conditions.append({
                "name": "Respiratory Infection",
                "probability": 0.60,
                "description": "Infection affecting the respiratory system",
                "common_symptoms": ["cough", "shortness_of_breath", "chest_pain", "fever"]
            })
        
        # Musculoskeletal issues
        if any(symptom in symptoms for symptom in ['muscle_pain', 'joint_pain', 'fatigue']):
            conditions.append({
                "name": "Viral Syndrome",
                "probability": 0.55,
                "description": "General viral infection causing body aches and fatigue",
                "common_symptoms": ["muscle_pain", "joint_pain", "fatigue", "fever"]
            })
        
        # If no specific patterns, provide general guidance
        if not conditions:
            conditions.append({
                "name": "General Malaise",
                "probability": 0.40,
                "description": "General feeling of discomfort or illness",
                "common_symptoms": symptoms
            })
        
        return sorted(conditions, key=lambda x: x['probability'], reverse=True)
    
    def _get_general_advice(self, symptoms: List[str], severity: str) -> List[str]:
        """Provide general health advice based on symptoms."""
        advice = []
        
        # General advice
        advice.append("Get plenty of rest and stay hydrated")
        advice.append("Monitor your symptoms and seek medical attention if they worsen")
        
        # Severity-based advice
        if severity == "severe":
            advice.append("Consider seeking immediate medical attention")
            advice.append("Contact your healthcare provider or visit an urgent care center")
        elif severity == "moderate":
            advice.append("Consider contacting your healthcare provider if symptoms persist")
            advice.append("Take over-the-counter medications as needed for symptom relief")
        else:  # mild
            advice.append("Home care and rest may be sufficient")
            advice.append("Monitor symptoms for any changes")
        
        # Symptom-specific advice
        if 'fever' in symptoms:
            advice.append("Use fever-reducing medications if needed and stay cool")
        
        if any(symptom in symptoms for symptom in ['cough', 'sore_throat']):
            advice.append("Consider throat lozenges and warm liquids for throat comfort")
        
        if any(symptom in symptoms for symptom in ['nausea', 'vomiting', 'diarrhea']):
            advice.append("Stay hydrated with clear fluids and avoid solid foods initially")
        
        if 'headache' in symptoms:
            advice.append("Rest in a quiet, dark room and consider pain relief medication")
        
        return advice
    
    def _assess_urgency(self, symptoms: List[str], severity: str) -> str:
        """Assess the urgency level of symptoms."""
        emergency_symptoms = ['chest_pain', 'shortness_of_breath', 'severe_headache']
        urgent_symptoms = ['high_fever', 'persistent_vomiting', 'severe_abdominal_pain']
        
        if any(symptom in symptoms for symptom in emergency_symptoms) or severity == "severe":
            return "high"
        elif any(symptom in symptoms for symptom in urgent_symptoms) or severity == "moderate":
            return "medium"
        else:
            return "low"
