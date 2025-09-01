import os
import logging
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

# Try to load dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Create the app
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Add custom Jinja2 filters
    @app.template_filter('from_json')
    def from_json_filter(value):
        """Convert JSON string to Python object"""
        if isinstance(value, str):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return []
        return value

    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///health_assistant.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Configure Stripe (with fallback values)
    app.config["STRIPE_PUBLISHABLE_KEY"] = os.environ.get("STRIPE_PUBLISHABLE_KEY", "pk_test_your_publishable_key_here")
    app.config["STRIPE_SECRET_KEY"] = os.environ.get("STRIPE_SECRET_KEY", "sk_test_your_secret_key_here")

    # Configure OpenAI (with fallback values)
    app.config["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "your_openai_api_key_here")

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))

    with app.app_context():
        # Import models to ensure tables are created
        import models
        db.create_all()
        
        # Import and register routes
        try:
            import routes
            # Register the routes blueprint
            app.register_blueprint(routes.bp)
        except ImportError as e:
            print(f"Warning: Some routes may not be available due to missing dependencies: {e}")
            # Import basic routes only
            from routes import login, register, logout, index, dashboard, symptoms, results, history, profile

    return app

# Create the app instance
app = create_app()

# Run the app if this file is executed directly
if __name__ == '__main__':
    print("=" * 60)
    print("🏥 Community Health Assistant")
    print("=" * 60)
    print("Starting server...")
    print("Visit: http://localhost:5000")
    print("=" * 60)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

