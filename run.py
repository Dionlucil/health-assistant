#!/usr/bin/env python3
"""
Health Assistant Flask Application Runner
"""

import os
import sys
from health_app import app

def main():
    """Main function to run the Flask application"""
    
    # Set environment variables if not already set
    if not os.environ.get('FLASK_ENV'):
        os.environ['FLASK_ENV'] = 'development'
    
    if not os.environ.get('FLASK_DEBUG'):
        os.environ['FLASK_DEBUG'] = '1'
    
    print("=" * 60)
    print("🏥 Community Health Assistant")
    print("=" * 60)
    print(f"Flask Environment: {os.environ.get('FLASK_ENV')}")
    print(f"Debug Mode: {os.environ.get('FLASK_DEBUG')}")
    print(f"Static Folder: {app.static_folder}")
    print(f"Static URL Path: {app.static_url_path}")
    print("=" * 60)
    print("Starting server...")
    print("Visit: http://localhost:5000")
    print("Debug static files: http://localhost:5000/debug-static")
    print("=" * 60)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
