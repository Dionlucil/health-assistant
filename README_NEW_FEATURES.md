# Health Assistant - New Features Setup Guide

This guide will help you set up the new AI doctor chat, payment system, and pricing features for your Health Assistant application.

## New Features Added

### 1. AI Doctor Chat
- Interactive chat with AI medical assistant (Dr. Sarah Chen)
- Symptom checklist before starting consultation
- Real-time medical advice and medication recommendations
- Medical-themed UI with doctor avatar

### 2. Payment System
- Stripe integration for secure payments
- Pricing plans: Single Consultation ($9.99), Monthly Premium ($29.99), Yearly Premium ($299.99)
- Free trial: 1 free consultation per user
- Payment required after free consultation is used

### 3. Enhanced Dashboard
- Payment status indicators
- Subscription information
- AI doctor quick access
- Enhanced consultation history with payment status

## Setup Instructions

### 1. Install New Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in your project root with the following variables:

```env
# Flask Configuration
SESSION_SECRET=your-super-secret-session-key
DATABASE_URL=sqlite:///health_assistant.db

# Stripe Configuration (Get from https://dashboard.stripe.com/apikeys)
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_SECRET_KEY=sk_test_your_secret_key_here

# OpenAI Configuration (Get from https://platform.openai.com/api-keys)
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run Database Migration

```bash
python migrate_db.py
```

This will:
- Add new columns to existing tables
- Create new tables for payments, chat sessions, and pricing
- Insert default pricing plans

### 4. Test the Application

```bash
python run.py
```

## Feature Details

### AI Doctor Chat (`/ai-doctor`)

**Features:**
- Medical-themed chat interface
- Symptom checklist (fever, headache, cough, fatigue, nausea, night sweats)
- Real-time AI responses with medical advice
- Medication recommendations
- Payment gate for non-subscribers

**How it works:**
1. User selects symptoms from checklist
2. Starts chat with AI doctor
3. AI provides medical guidance and recommendations
4. Payment required if free consultation used

### Payment System

**Pricing Plans:**
- **Single Consultation**: $9.99 (one-time)
- **Monthly Premium**: $29.99/month (10 consultations)
- **Yearly Premium**: $299.99/year (120 consultations, 17% savings)

**Payment Flow:**
1. User submits symptoms
2. System checks if payment required
3. If yes, redirects to payment page
4. After successful payment, shows AI analysis results

### Dashboard Enhancements

**New Features:**
- Payment status alerts
- Subscription information
- AI doctor quick access
- Enhanced consultation history
- Free consultation counter

## API Keys Required

### Stripe
1. Sign up at https://stripe.com
2. Go to Dashboard > API Keys
3. Copy your publishable and secret keys
4. Add to `.env` file

### OpenAI
1. Sign up at https://platform.openai.com
2. Go to API Keys section
3. Create a new API key
4. Add to `.env` file

## Testing

### Test Payment Flow
1. Register a new account
2. Use the free consultation
3. Try to access AI doctor again
4. Should see payment required message
5. Test payment with Stripe test card: 4242 4242 4242 4242

### Test AI Doctor
1. Go to `/ai-doctor`
2. Select symptoms from checklist
3. Start chat
4. Ask medical questions
5. Verify AI responses

## Security Notes

- All payments are processed securely through Stripe
- Health data is encrypted and protected
- AI responses are for informational purposes only
- Users are advised to consult real doctors for serious conditions

## Troubleshooting

### Common Issues

1. **Database migration errors**: Delete the existing database file and run migration again
2. **Stripe payment failures**: Check your Stripe keys and ensure you're using test keys for development
3. **AI not responding**: Verify your OpenAI API key and check API usage limits
4. **Payment not processing**: Ensure Stripe webhook endpoints are configured (for production)

### Error Messages

- "Payment required": User has used free consultation and needs to pay
- "Invalid API key": Check your OpenAI or Stripe API keys
- "Database error": Run migration script again

## Production Deployment

For production deployment:

1. Use production Stripe keys
2. Set up Stripe webhooks for payment confirmation
3. Use a production database (PostgreSQL recommended)
4. Set up proper SSL certificates
5. Configure proper session secrets
6. Set up monitoring and logging

## Support

If you encounter issues:
1. Check the error logs
2. Verify all API keys are correct
3. Ensure database migration completed successfully
4. Test with a fresh database if needed

## Medical Disclaimer

This application provides AI-powered health guidance for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions.
