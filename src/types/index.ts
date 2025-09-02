export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  age: number;
  gender: string;
  created_at: string;
  free_consultations_used: number;
  subscription_status: 'free' | 'premium';
  subscription_expires?: string;
}

export interface Consultation {
  id: string;
  user_id: string;
  symptoms: string[];
  severity: 'mild' | 'moderate' | 'severe';
  duration: string;
  additional_info?: string;
  analysis?: ConsultationAnalysis;
  created_at: string;
  payment_required: boolean;
  payment_status: 'pending' | 'paid' | 'free';
}

export interface ConsultationAnalysis {
  conditions: string[];
  medications: string[];
  advice: string[];
  urgency: 'low' | 'medium' | 'high';
  disclaimer: string;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  message_type: 'user' | 'ai';
  content: string;
  timestamp: string;
}

export interface ChatSession {
  id: string;
  user_id: string;
  session_id: string;
  created_at: string;
  last_activity: string;
  is_active: boolean;
}

export interface PricingPlan {
  id: string;
  name: string;
  price: number;
  currency: string;
  consultations_limit: number;
  duration_days: number;
  features: string[];
  is_active: boolean;
}

export interface AIResponse {
  response: string;
  medications: string[];
  advice: string[];
  timestamp: string;
  requires_follow_up: boolean;
}