import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

export type Database = {
  public: {
    Tables: {
      users: {
        Row: {
          id: string
          email: string
          first_name: string
          last_name: string
          age: number
          gender: string
          created_at: string
          free_consultations_used: number
          subscription_status: string
          subscription_expires: string | null
        }
        Insert: {
          id?: string
          email: string
          first_name: string
          last_name: string
          age: number
          gender: string
          created_at?: string
          free_consultations_used?: number
          subscription_status?: string
          subscription_expires?: string | null
        }
        Update: {
          id?: string
          email?: string
          first_name?: string
          last_name?: string
          age?: number
          gender?: string
          created_at?: string
          free_consultations_used?: number
          subscription_status?: string
          subscription_expires?: string | null
        }
      }
      consultations: {
        Row: {
          id: string
          user_id: string
          symptoms: string[]
          severity: string
          duration: string
          additional_info: string | null
          analysis: any
          created_at: string
          payment_required: boolean
          payment_status: string
        }
        Insert: {
          id?: string
          user_id: string
          symptoms: string[]
          severity: string
          duration: string
          additional_info?: string | null
          analysis?: any
          created_at?: string
          payment_required?: boolean
          payment_status?: string
        }
        Update: {
          id?: string
          user_id?: string
          symptoms?: string[]
          severity?: string
          duration?: string
          additional_info?: string | null
          analysis?: any
          created_at?: string
          payment_required?: boolean
          payment_status?: string
        }
      }
      chat_sessions: {
        Row: {
          id: string
          user_id: string
          session_id: string
          created_at: string
          last_activity: string
          is_active: boolean
        }
        Insert: {
          id?: string
          user_id: string
          session_id: string
          created_at?: string
          last_activity?: string
          is_active?: boolean
        }
        Update: {
          id?: string
          user_id?: string
          session_id?: string
          created_at?: string
          last_activity?: string
          is_active?: boolean
        }
      }
      chat_messages: {
        Row: {
          id: string
          session_id: string
          message_type: string
          content: string
          timestamp: string
        }
        Insert: {
          id?: string
          session_id: string
          message_type: string
          content: string
          timestamp?: string
        }
        Update: {
          id?: string
          session_id?: string
          message_type?: string
          content?: string
          timestamp?: string
        }
      }
    }
  }
}