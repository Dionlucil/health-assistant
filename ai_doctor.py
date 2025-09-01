import os
import json
from datetime import datetime
from typing import Dict, List, Optional

class AIDoctor:
    def __init__(self):
        # Medical knowledge base for common symptoms and conditions
        self.medical_knowledge = {
            "fever": {
                "conditions": ["Common cold", "Flu", "COVID-19", "Bacterial infection"],
                "medications": ["Acetaminophen", "Ibuprofen", "Aspirin"],
                "advice": "Rest, stay hydrated, monitor temperature"
            },
            "headache": {
                "conditions": ["Tension headache", "Migraine", "Sinusitis", "Dehydration"],
                "medications": ["Acetaminophen", "Ibuprofen", "Aspirin", "Caffeine"],
                "advice": "Rest in a quiet, dark room, stay hydrated"
            },
            "cough": {
                "conditions": ["Common cold", "Bronchitis", "Pneumonia", "Allergies"],
                "medications": ["Cough suppressants", "Expectorants", "Honey"],
                "advice": "Stay hydrated, use humidifier, avoid irritants"
            },
            "fatigue": {
                "conditions": ["Anemia", "Depression", "Sleep disorders", "Chronic fatigue"],
                "medications": ["Iron supplements", "Vitamin B12", "Melatonin"],
                "advice": "Improve sleep hygiene, exercise regularly, balanced diet"
            },
            "nausea": {
                "conditions": ["Gastritis", "Food poisoning", "Migraine", "Pregnancy"],
                "medications": ["Antiemetics", "Ginger", "Peppermint"],
                "advice": "Small frequent meals, avoid strong odors, rest"
            },
            "sore throat": {
                "conditions": ["Strep throat", "Viral infection", "Allergies", "Acid reflux"],
                "medications": ["Throat lozenges", "Salt water gargle", "Honey", "Pain relievers"],
                "advice": "Rest voice, stay hydrated, avoid irritants"
            },
            "runny nose": {
                "conditions": ["Common cold", "Allergies", "Sinusitis", "Viral infection"],
                "medications": ["Decongestants", "Antihistamines", "Saline spray"],
                "advice": "Stay hydrated, use humidifier, avoid allergens"
            },
            "muscle aches": {
                "conditions": ["Flu", "Overexertion", "Fibromyalgia", "Viral infection"],
                "medications": ["Ibuprofen", "Acetaminophen", "Muscle relaxants"],
                "advice": "Rest, gentle stretching, warm compress"
            },
            "dizziness": {
                "conditions": ["Dehydration", "Low blood pressure", "Inner ear problems", "Anxiety"],
                "medications": ["Anti-nausea medication", "Electrolytes"],
                "advice": "Stay hydrated, avoid sudden movements, rest"
            },
            "chest pain": {
                "conditions": ["Costochondritis", "Muscle strain", "Heartburn", "Anxiety"],
                "medications": ["Antacids", "Ibuprofen", "Pain relievers"],
                "advice": "Rest, avoid heavy meals, and monitor your symptoms. If pain is severe or radiates to your arm/jaw, seek immediate medical attention."
            },
            "difficulty breathing": {
                "conditions": ["Asthma", "Anxiety", "Respiratory infection", "Costochondritis"],
                "medications": ["Bronchodilators", "Anti-anxiety medication", "Pain relievers"],
                "advice": "Sit upright, practice deep breathing, avoid triggers"
            },
            "pain": {
                "conditions": ["Muscle strain", "Inflammation", "Nerve irritation", "Tissue damage"],
                "medications": ["Ibuprofen", "Acetaminophen", "Anti-inflammatory drugs"],
                "advice": "Rest the affected area, apply ice/heat, avoid aggravating movements"
            },
            "asthma": {
                "conditions": ["Asthma exacerbation", "Respiratory inflammation", "Bronchial spasm"],
                "medications": ["Albuterol inhaler", "Inhaled corticosteroids", "Bronchodilators"],
                "advice": "Use rescue inhaler as prescribed, avoid triggers, monitor symptoms"
            }
        }
        
        # Symptom variations and synonyms
        self.symptom_variations = {
            "chest pain": ["chest pain", "chest ache", "chest discomfort", "pain in chest", "left chest pain", "right chest pain"],
            "difficulty breathing": ["difficulty breathing", "breathing problems", "shortness of breath", "breathless", "can't breathe", "hard to breathe"],
            "pain": ["pain", "ache", "discomfort", "soreness", "tenderness", "hurts"],
            "asthma": ["asthma", "asthmatic", "breathing difficulty", "wheezing", "tight chest"]
        }
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for better symptom detection"""
        # Remove common filler words and normalize
        text = text.lower().strip()
        text = text.replace("i have", "").replace("i'm experiencing", "").replace("i feel", "")
        text = text.replace("am", "").replace("is", "").replace("are", "")
        return text
    
    def _detect_symptoms(self, user_message: str) -> List[str]:
        """Detect symptoms from user message"""
        detected_symptoms = []
        normalized_message = self._normalize_text(user_message)
        
        # Check for exact symptom matches
        for symptom in self.medical_knowledge.keys():
            if symptom in normalized_message:
                detected_symptoms.append(symptom)
        
        # Check for symptom variations
        for base_symptom, variations in self.symptom_variations.items():
            for variation in variations:
                if variation in normalized_message:
                    if base_symptom not in detected_symptoms:
                        detected_symptoms.append(base_symptom)
                    break
        
        # Check for specific pain locations
        if any(word in normalized_message for word in ["left side", "left chest", "left rib", "left boob", "left breast"]):
            if "chest pain" not in detected_symptoms:
                detected_symptoms.append("chest pain")
        
        if any(word in normalized_message for word in ["breathing", "breathe", "breath"]):
            if "difficulty breathing" not in detected_symptoms:
                detected_symptoms.append("difficulty breathing")
        
        return detected_symptoms
    
    def get_medical_response(self, user_message: str, chat_history: List[Dict] = None) -> Dict:
        """
        Get AI doctor response based on user message and chat history
        """
        user_message_lower = user_message.lower()
        
        # Check for greetings first
        if any(word in user_message_lower for word in ["how are you", "hello", "hi", "good morning", "good afternoon", "hey"]):
            return {
                "response": "Hello! I'm Dr. Sarah Chen, your AI medical assistant. I'm here to help you with your health concerns. Please describe your symptoms or ask any health-related questions. I'll provide you with medical guidance and treatment recommendations based on your symptoms.",
                "medications": [],
                "advice": ["I'm ready to help diagnose and treat your symptoms."],
                "timestamp": datetime.utcnow().isoformat(),
                "requires_follow_up": False
            }
        
        # Check for prescription requests
        if any(word in user_message_lower for word in ["prescription", "prescribe", "medicine", "medication", "treatment", "give me"]):
            # Look for symptoms in chat history or ask for them
            if chat_history and len(chat_history) > 1:
                # Analyze previous messages for symptoms
                all_text = " ".join([msg.get("message", "") for msg in chat_history if msg.get("role") == "user"])
                symptoms = self._detect_symptoms(all_text)
                if symptoms:
                    return self._provide_prescription(symptoms)
            
            return {
                "response": "I'd be happy to provide you with a prescription and treatment plan. To do this effectively, I need to understand your symptoms better. Could you please describe what you're experiencing? For example: chest pain, difficulty breathing, fever, etc.",
                "medications": [],
                "advice": ["Please describe your symptoms for prescription"],
                "timestamp": datetime.utcnow().isoformat(),
                "requires_follow_up": True
            }
        
        # Detect symptoms in the current message
        detected_symptoms = self._detect_symptoms(user_message)
        
        if detected_symptoms:
            return self._provide_symptom_analysis(detected_symptoms, user_message)
        
        # Check for specific symptom combinations
        if "chest pain" in user_message_lower and any(word in user_message_lower for word in ["sharp", "left", "rib", "boob", "breast"]):
            return {
                "response": "Based on your description of left-sided chest pain between your rib and breast area, this sounds like costochondritis (inflammation of rib cartilage) or muscle strain. As your doctor, I recommend taking ibuprofen 400mg every 6-8 hours, applying heat to the area, and avoiding sleeping on your left side. If the pain worsens or you develop shortness of breath, contact me immediately.",
                "medications": ["Ibuprofen 400mg", "Heat therapy"],
                "advice": ["Avoid sleeping on left side", "Apply heat to painful area", "Take ibuprofen as directed"],
                "timestamp": datetime.utcnow().isoformat(),
                "requires_follow_up": True
            }
        
        if "fever" in user_message_lower and "headache" in user_message_lower:
            return {
                "response": "You have a fever with headache, which suggests you're fighting an infection. As your doctor, I recommend rest, plenty of fluids, and acetaminophen or ibuprofen to reduce fever and pain. This is likely a viral infection that should resolve in 3-5 days. Let me know if you develop a stiff neck, severe headache, or rash.",
                "medications": ["Acetaminophen", "Ibuprofen"],
                "advice": ["Rest, fluids, fever management", "Monitor for severe symptoms"],
                "timestamp": datetime.utcnow().isoformat(),
                "requires_follow_up": True
            }
        
        # Check for emergency keywords
        if any(word in user_message_lower for word in ["emergency", "severe", "critical", "heart attack", "stroke", "bleeding"]):
            return {
                "response": "This sounds like a medical emergency. As your doctor, I need you to call emergency services (911) immediately or go to the nearest emergency room. Your symptoms require immediate medical attention.",
                "medications": [],
                "advice": ["Call emergency services immediately - this is urgent"],
                "timestamp": datetime.utcnow().isoformat(),
                "requires_follow_up": False
            }
        
        # Default response - ask for more details
        return {
            "response": "I understand you have health concerns. As your doctor, I'd like to help you better. Could you please describe your symptoms in more detail? Tell me about the severity, duration, and any other symptoms you're experiencing so I can provide you with a proper diagnosis and treatment plan.",
            "medications": [],
            "advice": ["Please provide more details about your symptoms for better diagnosis"],
            "timestamp": datetime.utcnow().isoformat(),
            "requires_follow_up": True
        }
    
    def _provide_symptom_analysis(self, symptoms: List[str], user_message: str) -> Dict:
        """Provide analysis for detected symptoms"""
        conditions = []
        medications = []
        advice = []
        
        for symptom in symptoms:
            if symptom in self.medical_knowledge:
                info = self.medical_knowledge[symptom]
                conditions.extend(info['conditions'][:2])
                medications.extend(info['medications'][:2])
                advice.append(info['advice'])
        
        # Special handling for chest pain with breathing difficulty
        if "chest pain" in symptoms and "difficulty breathing" in symptoms:
            response = "Based on your symptoms of chest pain and difficulty breathing, especially with your history of asthma, this could be costochondritis (inflammation of rib cartilage) or an asthma exacerbation. As your doctor, I recommend: 1) Use your asthma inhaler if prescribed, 2) Take ibuprofen 400mg every 6-8 hours for pain, 3) Avoid sleeping on your left side, 4) Apply heat to the painful area. Monitor your breathing - if it worsens, contact me immediately."
            medications = ["Ibuprofen 400mg", "Asthma inhaler (if prescribed)", "Heat therapy"]
            advice = ["Use asthma inhaler", "Avoid left side sleeping", "Apply heat therapy", "Monitor breathing"]
        else:
            response = f"Based on your symptoms, you appear to have {', '.join(conditions[:2])}. As your doctor, I recommend {advice[0] if advice else 'rest and monitoring'}. You can take {', '.join(medications[:2])} to help manage your symptoms. Let me know if your symptoms worsen or persist beyond a few days."
        
        return {
            "response": response,
            "medications": medications[:3],
            "advice": advice[:2],
            "timestamp": datetime.utcnow().isoformat(),
            "requires_follow_up": True
        }
    
    def _provide_prescription(self, symptoms: List[str]) -> Dict:
        """Provide prescription based on symptoms"""
        conditions = []
        medications = []
        advice = []
        
        for symptom in symptoms:
            if symptom in self.medical_knowledge:
                info = self.medical_knowledge[symptom]
                conditions.extend(info['conditions'][:2])
                medications.extend(info['medications'][:2])
                advice.append(info['advice'])
        
        if not conditions:
            conditions = ["General health concern"]
            advice = ["Rest and monitor symptoms"]
        
        return {
            "response": f"Based on your symptoms, here's your prescription: {', '.join(medications[:3])}. Take as directed for {', '.join(conditions[:2])}. {advice[0] if advice else 'Rest and monitor your symptoms'}. Follow up with me if symptoms persist or worsen.",
            "medications": medications[:3],
            "advice": advice[:2],
            "timestamp": datetime.utcnow().isoformat(),
            "requires_follow_up": False
        }
    
    def analyze_symptoms_for_prescription(self, symptoms: List[str], age: int, gender: str) -> Dict:
        """
        Analyze symptoms and provide prescription recommendations
        """
        conditions = []
        medications = []
        advice = []
        
        for symptom in symptoms:
            symptom_lower = symptom.lower().strip()
            if symptom_lower in self.medical_knowledge:
                info = self.medical_knowledge[symptom_lower]
                conditions.extend(info['conditions'][:2])
                medications.extend(info['medications'][:2])
                advice.append(info['advice'])
        
        if not conditions:
            conditions = ["General health concern"]
            advice = ["Rest and monitor symptoms"]
        
        return {
            "analysis": {
                "conditions": list(set(conditions))[:3],
                "medications": list(set(medications))[:3],
                "advice": list(set(advice))[:2],
                "warnings": ["Monitor symptoms and follow up if they worsen"]
            },
            "timestamp": datetime.utcnow().isoformat(),
            "confidence_level": self._calculate_confidence(symptoms)
        }
    
    def _calculate_confidence(self, symptoms: List[str]) -> str:
        """Calculate confidence level based on symptom clarity"""
        if len(symptoms) >= 3:
            return "high"
        elif len(symptoms) >= 2:
            return "medium"
        else:
            return "low"
    
    def get_follow_up_questions(self, symptoms: List[str]) -> List[str]:
        """Get follow-up questions to better understand the patient's condition"""
        questions = []
        symptoms_lower = [s.lower() for s in symptoms]
        
        if "chest pain" in symptoms_lower:
            questions.extend([
                "How long have you had this chest pain?",
                "Does the pain worsen with movement or breathing?",
                "Are you experiencing any shortness of breath?",
                "Does the pain radiate to your arm, jaw, or back?"
            ])
        
        if "fever" in symptoms_lower:
            questions.extend([
                "What's your temperature?",
                "How long have you had the fever?",
                "Are you experiencing chills or sweating?",
                "Do you have any other symptoms like cough or sore throat?"
            ])
        
        if "headache" in symptoms_lower:
            questions.extend([
                "Where exactly is the headache located?",
                "How severe is the pain on a scale of 1-10?",
                "What makes it better or worse?",
                "Do you have any visual changes or nausea?"
            ])
        
        return questions[:3]  # Return max 3 questions
