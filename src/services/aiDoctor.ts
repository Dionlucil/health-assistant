import { AIResponse } from '../types'

export class AIDoctor {
  private medicalKnowledge = {
    fever: {
      conditions: ['Common cold', 'Flu', 'COVID-19', 'Bacterial infection'],
      medications: ['Acetaminophen', 'Ibuprofen', 'Aspirin'],
      advice: 'Rest, stay hydrated, monitor temperature'
    },
    headache: {
      conditions: ['Tension headache', 'Migraine', 'Sinusitis', 'Dehydration'],
      medications: ['Acetaminophen', 'Ibuprofen', 'Aspirin', 'Caffeine'],
      advice: 'Rest in a quiet, dark room, stay hydrated'
    },
    cough: {
      conditions: ['Common cold', 'Bronchitis', 'Pneumonia', 'Allergies'],
      medications: ['Cough suppressants', 'Expectorants', 'Honey'],
      advice: 'Stay hydrated, use humidifier, avoid irritants'
    },
    fatigue: {
      conditions: ['Anemia', 'Depression', 'Sleep disorders', 'Chronic fatigue'],
      medications: ['Iron supplements', 'Vitamin B12', 'Melatonin'],
      advice: 'Improve sleep hygiene, exercise regularly, balanced diet'
    },
    nausea: {
      conditions: ['Gastritis', 'Food poisoning', 'Migraine', 'Pregnancy'],
      medications: ['Antiemetics', 'Ginger', 'Peppermint'],
      advice: 'Small frequent meals, avoid strong odors, rest'
    },
    chest_pain: {
      conditions: ['Costochondritis', 'Muscle strain', 'Anxiety', 'Heart condition'],
      medications: ['Ibuprofen', 'Acetaminophen', 'Muscle relaxants'],
      advice: 'Rest, avoid heavy lifting, warm compress'
    }
  }

  private symptomVariations = {
    'chest pain': ['chest pain', 'chest ache', 'chest discomfort', 'pain in chest'],
    'difficulty breathing': ['difficulty breathing', 'breathing problems', 'shortness of breath', 'breathless'],
    'pain': ['pain', 'ache', 'discomfort', 'soreness', 'tenderness', 'hurts']
  }

  private normalizeText(text: string): string {
    text = text.toLowerCase().trim()
    text = text.replace(/i have|i'm experiencing|i feel|am|is|are/g, '')
    return text
  }

  private detectSymptoms(userMessage: string): string[] {
    const detectedSymptoms: string[] = []
    const normalizedMessage = this.normalizeText(userMessage)

    // Check for exact symptom matches
    for (const symptom of Object.keys(this.medicalKnowledge)) {
      if (normalizedMessage.includes(symptom)) {
        detectedSymptoms.push(symptom)
      }
    }

    // Check for symptom variations
    for (const [baseSymptom, variations] of Object.entries(this.symptomVariations)) {
      for (const variation of variations) {
        if (normalizedMessage.includes(variation)) {
          if (!detectedSymptoms.includes(baseSymptom)) {
            detectedSymptoms.push(baseSymptom)
          }
          break
        }
      }
    }

    return detectedSymptoms
  }

  public getMedicalResponse(userMessage: string, chatHistory: any[] = []): AIResponse {
    const userMessageLower = userMessage.toLowerCase()

    // Handle greetings
    if (['hello', 'hi', 'hey', 'good morning', 'good afternoon'].some(word => 
      userMessageLower.includes(word)) && chatHistory.length === 0) {
      return {
        response: "Hello! I'm Dr. Sarah Chen, your AI medical assistant. I'm here to help you with your health concerns. Please describe your symptoms or ask any health-related questions.",
        medications: [],
        advice: ["I'm ready to help diagnose and treat your symptoms."],
        timestamp: new Date().toISOString(),
        requires_follow_up: false
      }
    }

    // Detect symptoms
    const detectedSymptoms = this.detectSymptoms(userMessage)

    if (detectedSymptoms.length > 0) {
      return this.provideSymptomAnalysis(detectedSymptoms, userMessage)
    }

    // Handle emergency keywords
    if (['emergency', 'severe', 'critical', 'heart attack', 'stroke', 'bleeding'].some(word => 
      userMessageLower.includes(word))) {
      return {
        response: "This sounds like a medical emergency. Please call emergency services (911) immediately or go to the nearest emergency room. Your symptoms require immediate medical attention.",
        medications: [],
        advice: ["Call emergency services immediately - this is urgent"],
        timestamp: new Date().toISOString(),
        requires_follow_up: false
      }
    }

    // Default response
    return {
      response: "I understand you have health concerns. Could you please describe your symptoms in more detail? Tell me about any pain, fever, nausea, or other discomfort you're experiencing.",
      medications: [],
      advice: ["Please provide more details about your symptoms for better diagnosis"],
      timestamp: new Date().toISOString(),
      requires_follow_up: true
    }
  }

  private provideSymptomAnalysis(symptoms: string[], userMessage: string): AIResponse {
    const conditions: string[] = []
    const medications: string[] = []
    const advice: string[] = []

    for (const symptom of symptoms) {
      if (symptom in this.medicalKnowledge) {
        const info = this.medicalKnowledge[symptom as keyof typeof this.medicalKnowledge]
        conditions.push(...info.conditions.slice(0, 2))
        medications.push(...info.medications.slice(0, 2))
        advice.push(info.advice)
      }
    }

    const response = `Based on your symptoms, you appear to have ${conditions.slice(0, 2).join(', ')}. I recommend ${advice[0] || 'rest and monitoring'}. You can take ${medications.slice(0, 2).join(', ')} to help manage your symptoms. Let me know if your symptoms worsen or persist beyond a few days.`

    return {
      response,
      medications: medications.slice(0, 3),
      advice: advice.slice(0, 2),
      timestamp: new Date().toISOString(),
      requires_follow_up: true
    }
  }

  public analyzeSymptoms(symptoms: string[], age: number, gender: string): any {
    const conditions: string[] = []
    const medications: string[] = []
    const advice: string[] = []

    for (const symptom of symptoms) {
      if (symptom in this.medicalKnowledge) {
        const info = this.medicalKnowledge[symptom as keyof typeof this.medicalKnowledge]
        conditions.push(...info.conditions.slice(0, 2))
        medications.push(...info.medications.slice(0, 2))
        advice.push(info.advice)
      }
    }

    return {
      analysis: {
        conditions: [...new Set(conditions)].slice(0, 3),
        medications: [...new Set(medications)].slice(0, 3),
        advice: [...new Set(advice)].slice(0, 2),
        warnings: ["Monitor symptoms and follow up if they worsen"]
      },
      timestamp: new Date().toISOString(),
      confidence_level: this.calculateConfidence(symptoms)
    }
  }

  private calculateConfidence(symptoms: string[]): string {
    if (symptoms.length >= 3) return 'high'
    if (symptoms.length >= 2) return 'medium'
    return 'low'
  }
}