#!/usr/bin/env python3
"""
Database migration script for Health Assistant
Adds new tables and columns for AI doctor, payments, and pricing features
"""

import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, text
from app import app, db
from models import User, Consultation, Payment, ChatSession, ChatMessage, PricingPlan

def migrate_database():
    """Migrate the database to add new features"""
    print("Starting database migration...")
    
    with app.app_context():
        # Get database engine
        engine = db.engine
        
        try:
            # Check if new columns exist
            inspector = db.inspect(engine)
            existing_tables = inspector.get_table_names()
            
            print(f"Existing tables: {existing_tables}")
            
            # Add new columns to User table if they don't exist
            if 'user' in existing_tables:
                columns = [col['name'] for col in inspector.get_columns('user')]
                
                if 'free_consultations_used' not in columns:
                    print("Adding free_consultations_used column to user table...")
                    engine.execute(text("ALTER TABLE user ADD COLUMN free_consultations_used INTEGER DEFAULT 0"))
                
                if 'subscription_status' not in columns:
                    print("Adding subscription_status column to user table...")
                    engine.execute(text("ALTER TABLE user ADD COLUMN subscription_status VARCHAR(20) DEFAULT 'free'"))
                
                if 'subscription_expires' not in columns:
                    print("Adding subscription_expires column to user table...")
                    engine.execute(text("ALTER TABLE user ADD COLUMN subscription_expires DATETIME"))
            
            # Add new columns to Consultation table if they don't exist
            if 'consultation' in existing_tables:
                columns = [col['name'] for col in inspector.get_columns('consultation')]
                
                if 'payment_required' not in columns:
                    print("Adding payment_required column to consultation table...")
                    engine.execute(text("ALTER TABLE consultation ADD COLUMN payment_required BOOLEAN DEFAULT FALSE"))
                
                if 'payment_status' not in columns:
                    print("Adding payment_status column to consultation table...")
                    engine.execute(text("ALTER TABLE consultation ADD COLUMN payment_status VARCHAR(20) DEFAULT 'pending'"))
            
            # Create new tables
            print("Creating new tables...")
            db.create_all()
            
            # Insert default pricing plans
            print("Inserting default pricing plans...")
            plans = [
                {
                    'name': 'Single Consultation',
                    'price': 9.99,
                    'currency': 'USD',
                    'consultations_limit': 1,
                    'duration_days': 1,
                    'features': '["1 AI Medical Consultation", "Symptom Analysis", "Medication Recommendations", "Health Advice", "24/7 Access"]',
                    'is_active': True
                },
                {
                    'name': 'Monthly Premium',
                    'price': 29.99,
                    'currency': 'USD',
                    'consultations_limit': 10,
                    'duration_days': 30,
                    'features': '["10 AI Consultations", "Priority Support", "Detailed Health Reports", "Medication Tracking", "Health History", "24/7 AI Doctor Access"]',
                    'is_active': True
                },
                {
                    'name': 'Yearly Premium',
                    'price': 299.99,
                    'currency': 'USD',
                    'consultations_limit': 120,
                    'duration_days': 365,
                    'features': '["120 AI Consultations", "Priority Support", "Advanced Health Analytics", "Medication Management", "Health Trends", "24/7 AI Doctor Access", "Save 17% vs Monthly"]',
                    'is_active': True
                }
            ]
            
            for plan_data in plans:
                existing_plan = PricingPlan.query.filter_by(name=plan_data['name']).first()
                if not existing_plan:
                    plan = PricingPlan(**plan_data)
                    db.session.add(plan)
            
            db.session.commit()
            print("Default pricing plans inserted successfully!")
            
            print("Database migration completed successfully!")
            
        except Exception as e:
            print(f"Error during migration: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    migrate_database()
