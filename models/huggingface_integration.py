"""
Hugging Face Model Integration for Health Assistant
This module provides a simple interface to use Hugging Face models for medical text analysis.
"""

import os
import json
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceModelManager:
    """
    Manages Hugging Face models for medical text analysis.
    Provides fallback functionality when models are not available.
    """
    
    def __init__(self, model_path: str = "models/medical_model"):
        self.model_path = model_path
        self.model_loaded = False
        self.model = None
        self.tokenizer = None
        
        # Try to load the model
        self._load_model()
    
    def _load_model(self):
        """Attempt to load the Hugging Face model"""
        try:
            # Check if transformers is available
            import transformers
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            
            # Check if model directory exists
            if os.path.exists(self.model_path):
                logger.info(f"Loading model from {self.model_path}")
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
                self.model_loaded = True
                logger.info("Model loaded successfully")
            else:
                logger.warning(f"Model directory {self.model_path} not found. Using fallback mode.")
                
        except ImportError:
            logger.warning("Transformers library not available. Using fallback mode.")
        except Exception as e:
            logger.error(f"Error loading model: {e}. Using fallback mode.")
    
    def analyze_symptoms(self, symptoms_text: str) -> Dict[str, any]:
        """
        Analyze symptoms using the loaded model or fallback to basic analysis
        
        Args:
            symptoms_text (str): Text describing symptoms
            
        Returns:
            Dict containing analysis results
        """
        if self.model_loaded and self.model and self.tokenizer:
            return self._analyze_with_model(symptoms_text)
        else:
            return self._fallback_analysis(symptoms_text)
    
    def _analyze_with_model(self, symptoms_text: str) -> Dict[str, any]:
        """Analyze symptoms using the loaded Hugging Face model"""
        try:
            # Tokenize input
            inputs = self.tokenizer(
                symptoms_text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=512,
                padding=True
            )
            
            # Get model predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.softmax(outputs.logits, dim=-1)
            
            # Convert to probabilities
            probs = predictions[0].tolist()
            
            # Get predicted class
            predicted_class = torch.argmax(predictions, dim=-1).item()
            
            return {
                "model_used": True,
                "confidence": max(probs),
                "predicted_class": predicted_class,
                "probabilities": probs,
                "analysis": f"Model analysis: Class {predicted_class} with {max(probs):.2%} confidence"
            }
            
        except Exception as e:
            logger.error(f"Error in model analysis: {e}")
            return self._fallback_analysis(symptoms_text)
    
    def _fallback_analysis(self, symptoms_text: str) -> Dict[str, any]:
        """Fallback analysis when model is not available"""
        symptoms_lower = symptoms_text.lower()
        
        # Basic symptom analysis
        analysis = {
            "model_used": False,
            "confidence": 0.6,
            "analysis": "Basic symptom analysis (model not available)",
            "symptoms_detected": [],
            "potential_conditions": [],
            "recommendations": []
        }
        
        # Detect common symptoms
        common_symptoms = {
            "fever": ["fever", "temperature", "hot", "burning"],
            "headache": ["headache", "head pain", "migraine"],
            "cough": ["cough", "coughing", "dry cough", "wet cough"],
            "fatigue": ["fatigue", "tired", "exhausted", "weak"],
            "nausea": ["nausea", "sick", "vomiting", "queasy"],
            "pain": ["pain", "ache", "sore", "hurt"],
            "swelling": ["swelling", "swollen", "inflammation"],
            "rash": ["rash", "redness", "itchy", "skin"]
        }
        
        detected_symptoms = []
        for symptom, keywords in common_symptoms.items():
            if any(keyword in symptoms_lower for keyword in keywords):
                detected_symptoms.append(symptom)
        
        analysis["symptoms_detected"] = detected_symptoms
        
        # Basic condition mapping
        if "fever" in detected_symptoms and "cough" in detected_symptoms:
            analysis["potential_conditions"].append("Common cold or flu")
            analysis["recommendations"].append("Rest, fluids, over-the-counter cold medicine")
        
        if "headache" in detected_symptoms and "fatigue" in detected_symptoms:
            analysis["potential_conditions"].append("Stress or tension headache")
            analysis["recommendations"].append("Rest, hydration, stress management")
        
        if "pain" in detected_symptoms and "swelling" in detected_symptoms:
            analysis["potential_conditions"].append("Inflammation or injury")
            analysis["recommendations"].append("Ice, rest, elevation, consider medical evaluation")
        
        # General recommendations
        if not analysis["recommendations"]:
            analysis["recommendations"].append("Monitor symptoms and seek medical attention if they worsen")
            analysis["recommendations"].append("Keep a symptom diary")
        
        return analysis
    
    def get_model_info(self) -> Dict[str, any]:
        """Get information about the loaded model"""
        return {
            "model_loaded": self.model_loaded,
            "model_path": self.model_path,
            "model_type": "Hugging Face Transformers" if self.model_loaded else "Fallback Mode",
            "capabilities": [
                "Symptom analysis",
                "Condition prediction",
                "Treatment recommendations"
            ] if self.model_loaded else [
                "Basic symptom detection",
                "Simple condition mapping",
                "General recommendations"
            ]
        }

# Global model manager instance
model_manager = HuggingFaceModelManager()

def analyze_symptoms_with_model(symptoms_text: str) -> Dict[str, any]:
    """
    Convenience function to analyze symptoms using the model manager
    
    Args:
        symptoms_text (str): Text describing symptoms
        
    Returns:
        Dict containing analysis results
    """
    return model_manager.analyze_symptoms(symptoms_text)

def get_model_status() -> Dict[str, any]:
    """
    Get the current status of the model
    
    Returns:
        Dict containing model status information
    """
    return model_manager.get_model_info()

if __name__ == "__main__":
    # Test the model manager
    test_symptoms = "I have a fever and headache, feeling very tired"
    result = analyze_symptoms_with_model(test_symptoms)
    print("Model Status:", get_model_status())
    print("Analysis Result:", json.dumps(result, indent=2))
