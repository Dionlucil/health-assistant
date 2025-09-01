# 🏥 Health Assistant - AI-Powered Medical Consultation Platform

A comprehensive Flask-based web application that provides AI-powered medical consultations, symptom analysis, and health guidance. Built with modern web technologies and featuring an intelligent AI doctor chatbot.

## 🌟 Features

### 🤖 AI Doctor Chat System
- **Intelligent Medical Assistant**: Dr. Diana, an AI-powered medical consultant
- **Natural Conversation Flow**: Human-like responses with empathetic tone
- **Symptom Analysis**: Comprehensive symptom database with 15+ conditions
- **Prescription Generation**: Specific medication recommendations with dosages
- **Real-time Chat Interface**: Modern, responsive chat UI with typing indicators

### 👤 User Authentication & Management
- **Secure Registration/Login**: Email-based authentication with password hashing
- **Session Management**: Persistent login sessions with Flask-Login
- **User Profiles**: Complete user information management
- **File-based Storage**: Persistent user data using pickle serialization

### 💳 Payment & Subscription System
- **Free Trial**: One free consultation per user
- **Payment Wall**: Automatic payment requirement after free consultation
- **Pricing Plans**: Flexible subscription options
- **Usage Tracking**: Monitor consultation usage and subscription status

### 📊 Dashboard & Analytics
- **Personal Dashboard**: User statistics and consultation history
- **Consultation History**: Track all past medical consultations
- **Payment Status**: Monitor subscription and payment information
- **Quick Actions**: Easy access to all features

### 🔍 Symptom Checker
- **Comprehensive Database**: 15+ symptoms with detailed analysis
- **Smart Matching**: Advanced symptom recognition with variations
- **Condition Detection**: Automatic disease identification
- **Treatment Recommendations**: Specific medications and dosages

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd HealthAssistant
```

2. **Install dependencies**
```bash
pip install flask flask-sqlalchemy flask-login werkzeug
```

3. **Run the application**
```bash
python app.py
```

4. **Access the application**
Open your browser and navigate to: `http://localhost:5000`

## 📁 Project Structure

```
HealthAssistant/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── forms.py               # Flask-WTF forms
├── users_data.pkl         # User data storage
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── login.html        # Login form
│   ├── register.html     # Registration form
│   ├── dashboard.html    # User dashboard
│   ├── ai_doctor.html    # AI Doctor chat interface
│   ├── symptoms.html     # Symptom checker
│   ├── pricing.html      # Pricing plans
│   ├── history.html      # Consultation history
│   ├── results.html      # Consultation results
│   └── profile.html      # User profile
├── static/               # Static files
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript files
└── README.md            # This file
```

## 🎯 Core Features Explained

### AI Doctor Chat System

The AI Doctor (Dr. Diana) provides intelligent medical consultations with:

**Symptom Database:**
- Headache, Fever, Cough, Chest Pain
- Fatigue, Nausea, Sore Throat, Runny Nose
- Muscle Aches, Vaginal Discharge, Dizziness
- Stomachache, Back Pain, Diarrhea

**Response Types:**
- **Greeting**: Natural conversation starters
- **Diagnosis**: Medical condition identification
- **Prescription**: Specific medication recommendations
- **Clarification**: Follow-up questions and explanations
- **Gratitude**: Polite conversation endings

**Example Conversation:**
```
Patient: "I feel dizzy and have stomachache"
Dr. Diana: "I understand you're experiencing dizziness and stomachache. Based on your symptoms, you may be experiencing Gastritis and Vertigo.

My Prescription:
MEDICATIONS: For gastritis: Antacids (Tums, Rolaids) OR Famotidine (Pepcid) 20mg twice daily. For dizziness: Meclizine (Bonine) 25mg daily for vertigo...

Would you like me to explain the dosage or any side effects?"
```

### User Authentication System

**Registration Process:**
1. User provides email, name, age, gender, password
2. Password is securely hashed using Werkzeug
3. User data is saved to `users_data.pkl`
4. Automatic login after successful registration

**Login Process:**
1. Email and password verification
2. Session creation with Flask-Login
3. Persistent sessions with `remember=True`
4. Automatic redirect to dashboard

**User Data Storage:**
- File-based persistence using pickle
- Automatic loading on application startup
- Secure password hashing
- User statistics tracking

### Payment & Subscription System

**Free Trial:**
- One free consultation per user
- Tracked via `free_consultations_used` counter
- Automatic payment wall after free consultation

**Payment Wall:**
- Appears when user requests diagnosis after free consultation
- Visual warning with payment options
- Direct link to pricing page
- User-friendly dismissal option

**Usage Tracking:**
- Monitor consultation usage
- Track subscription status
- Payment history (when implemented)

## 🔧 Configuration

### Application Settings
```python
# In app.py
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_assistant.db'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

### User Storage
```python
# File-based user storage
USERS_FILE = 'users_data.pkl'

def load_users():
    """Load users from file on startup"""
    
def save_users(users_db, user_id_counter):
    """Save users to file after changes"""
```

## 🎨 User Interface

### Modern Design Features
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Bootstrap Integration**: Professional UI components
- **Chat Interface**: Real-time messaging with typing indicators
- **Color-coded Messages**: AI messages (blue), User messages (green)
- **Quick Actions**: Symptom buttons for easy input
- **Payment Wall**: Visual payment requirement notifications

### Navigation
- **Home Page**: Welcome and feature overview
- **Login/Register**: User authentication
- **Dashboard**: Personal statistics and quick access
- **AI Doctor**: Chat interface for medical consultations
- **Symptom Checker**: Form-based symptom analysis
- **Pricing**: Subscription plans and payment options
- **History**: Past consultation records
- **Profile**: User account management

## 🔒 Security Features

### Authentication Security
- **Password Hashing**: Werkzeug secure password hashing
- **Session Management**: Flask-Login secure sessions
- **CSRF Protection**: Built-in Flask CSRF protection
- **Secure Cookies**: HTTPOnly and SameSite cookie settings

### Data Protection
- **File-based Storage**: Local user data storage
- **Input Validation**: Form validation and sanitization
- **Error Handling**: Graceful error handling and user feedback
- **Medical Disclaimers**: Clear disclaimers about AI limitations

## 📱 API Endpoints

### Authentication Routes
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /logout` - User logout

### Main Application Routes
- `GET /` - Home page
- `GET /dashboard` - User dashboard
- `GET /ai_doctor` - AI Doctor chat interface
- `POST /ai_doctor/chat` - AI Doctor chat API
- `GET /symptoms` - Symptom checker
- `GET /pricing` - Pricing plans
- `GET /history` - Consultation history
- `GET /profile` - User profile

### API Response Format
```json
{
  "response": "AI Doctor response text",
  "type": "diagnosis|greeting|clarification|gratitude",
  "diagnosis": {
    "disease": "Condition name",
    "prescription": "Treatment details",
    "severity": "mild|moderate|severe",
    "matched_symptoms": ["symptom1", "symptom2"]
  },
  "payment_required": false
}
```

## 🧪 Testing

### Manual Testing Steps

1. **User Registration**
   - Register a new account
   - Verify automatic login
   - Check user data persistence

2. **AI Doctor Chat**
   - Start a conversation
   - Test symptom recognition
   - Verify prescription generation
   - Test payment wall after free consultation

3. **Authentication**
   - Logout and login again
   - Verify session persistence
   - Test password validation

4. **Payment System**
   - Use free consultation
   - Verify payment wall appears
   - Test pricing page access

### Test Scenarios

**Scenario 1: New User Journey**
1. Register → Login → Dashboard → AI Doctor → Free Consultation → Payment Wall

**Scenario 2: Returning User**
1. Login → Dashboard → AI Doctor → Payment Required → Pricing Page

**Scenario 3: Symptom Analysis**
1. Symptoms Page → AI Doctor → Specific Symptoms → Diagnosis → Prescription

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production Considerations
1. **Environment Variables**: Set production SECRET_KEY
2. **Database**: Use PostgreSQL for production
3. **HTTPS**: Enable SSL certificates
4. **Session Security**: Set SESSION_COOKIE_SECURE=True
5. **Payment Integration**: Implement real payment processing
6. **Monitoring**: Add logging and error tracking

## 🔮 Future Enhancements

### Planned Features
- **Real Payment Processing**: Stripe/PayPal integration
- **Database Migration**: Move from file-based to SQL database
- **Email Notifications**: Consultation reminders and updates
- **Mobile App**: React Native or Flutter mobile application
- **Advanced AI**: Integration with OpenAI GPT for more sophisticated responses
- **Telemedicine**: Video consultation features
- **Prescription Management**: Digital prescription tracking
- **Health Records**: Comprehensive medical history management

### Technical Improvements
- **API Documentation**: Swagger/OpenAPI documentation
- **Unit Tests**: Comprehensive test coverage
- **CI/CD Pipeline**: Automated testing and deployment
- **Docker Support**: Containerized deployment
- **Microservices**: Break down into smaller services
- **Caching**: Redis for session and data caching

## 📞 Support & Contact

### Getting Help
- Check the terminal logs for debugging information
- Verify user data in `users_data.pkl`
- Test with fresh user registration
- Review error messages in browser console

### Common Issues
1. **Login Problems**: Check user data file and password hashing
2. **AI Not Responding**: Verify symptom database and response logic
3. **Payment Wall Issues**: Check free consultation tracking
4. **Session Problems**: Verify Flask-Login configuration

## ⚖️ Medical Disclaimer

**IMPORTANT**: This application provides AI-powered health guidance for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions. The AI responses are generated based on a limited symptom database and should not be considered as definitive medical advice.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Built with ❤️ using Flask, Python, and modern web technologies**
