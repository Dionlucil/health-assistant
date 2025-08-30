# Community Health Assistant

## Overview

Community Health Assistant is a web-based health assessment platform that provides users with AI-powered symptom analysis and health insights. The application allows users to check their symptoms through an interactive form, receive personalized health recommendations, and track their consultation history. Built as a comprehensive health tool, it emphasizes the importance of professional medical advice while providing valuable preliminary health information.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
The application uses a **Flask-based MVC architecture** with the following key components:
- **Flask** as the web framework with SQLAlchemy for database operations
- **SQLite/PostgreSQL** database with Flask-SQLAlchemy ORM for data persistence
- **Flask-Login** for user authentication and session management
- **Flask-WTF** for form handling and CSRF protection
- **Werkzeug** for password hashing and security

### Frontend Architecture
The frontend follows a **server-side rendered approach** with modern enhancements:
- **Jinja2 templating** for dynamic HTML generation
- **Bootstrap 5** for responsive UI components and styling
- **Font Awesome** for iconography
- **Custom CSS** for brand-specific styling and enhanced user experience
- **Vanilla JavaScript** for interactive features and form enhancements

### Database Design
The application uses a **relational database schema** with three main entities:
- **User model**: Stores user authentication data and profile information (email, password, personal details)
- **Consultation model**: Records symptom assessments with JSON-stored symptoms and analysis results
- **Symptom model**: Catalogs available symptoms with categories and descriptions

### Authentication System
Implements **session-based authentication** using Flask-Login:
- Password hashing with Werkzeug's security functions
- User session management with remember-me functionality
- Login required decorators for protected routes
- Secure user registration with email validation

### Symptom Analysis Engine
Features a **rule-based symptom analyzer** that:
- Maps symptom combinations to possible medical conditions
- Provides urgency assessments (low, medium, high priority)
- Generates personalized health advice and recommendations
- Includes comprehensive medical disclaimers

### Form Processing
Uses **WTForms for robust form handling**:
- Multi-checkbox symptom selection with validation
- User registration and login forms with proper validation
- Profile management forms for user data updates
- CSRF protection on all forms

## External Dependencies

### Core Framework Dependencies
- **Flask 3.1.2**: Web application framework
- **Flask-SQLAlchemy 3.1.1**: Database ORM integration
- **Flask-Login 0.6.3**: User session management
- **Flask-WTF 1.2.2**: Form handling and validation
- **WTForms**: Form validation and rendering

### Frontend Dependencies
- **Bootstrap 5.1.3 (CDN)**: CSS framework for responsive design
- **Font Awesome 6.0.0 (CDN)**: Icon library
- **Custom CSS/JS**: Application-specific styling and interactions

### Security and Utilities
- **Werkzeug**: Password hashing and WSGI utilities
- **ProxyFix middleware**: Request handling for deployment environments

### Development and Production
- **SQLite**: Default development database
- **PostgreSQL**: Production database option via DATABASE_URL environment variable
- **Environment variable configuration**: For sensitive data and deployment settings

### Potential Future Integrations
The architecture supports integration with:
- **Medical APIs** (Infermedica, WebMD API) for enhanced symptom analysis
- **Email services** for notifications and password reset
- **Analytics platforms** for user behavior tracking
- **External authentication providers** (OAuth)