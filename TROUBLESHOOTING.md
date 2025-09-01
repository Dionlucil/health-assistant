# Troubleshooting Guide - Health Assistant Flask App

## Issue: Styling Not Working

If the styling is not being applied to your Flask app, follow these steps:

### 1. Check Static File Configuration

The Flask app is configured to serve static files from the `static/` directory. Make sure:

- Static files are in the correct location: `static/css/style.css` and `static/js/main.js`
- The Flask app is configured with: `app = Flask(__name__, static_folder='static', static_url_path='/static')`

### 2. Run the App Correctly

Use one of these methods to run the app:

**Method 1: Use the run script**
```bash
python run.py
```

**Method 2: Use main.py**
```bash
python main.py
```

**Method 3: Use Flask CLI**
```bash
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1
flask run
```

### 3. Test Static File Serving

Visit these URLs to test if static files are working:

- `http://localhost:5000/debug-static` - Check if static files exist
- `http://localhost:5000/test-css` - Test CSS loading
- `http://localhost:5000/test` - Test static file serving

### 4. Check Browser Developer Tools

1. Open your browser's Developer Tools (F12)
2. Go to the Network tab
3. Refresh the page
4. Look for any failed requests to CSS or JS files
5. Check the Console tab for any JavaScript errors

### 5. Common Issues and Solutions

**Issue: CSS not loading**
- Check if the CSS file path is correct
- Verify the Flask app is configured for static files
- Check browser cache (Ctrl+F5 to force refresh)

**Issue: JavaScript not working**
- Check if the JS file path is correct
- Look for JavaScript errors in browser console
- Verify Bootstrap JS is loaded

**Issue: Bootstrap not working**
- Check if Bootstrap CDN links are accessible
- Verify internet connection for CDN resources
- Check if Bootstrap JS is loaded after CSS

### 6. File Structure Verification

Your project should have this structure:
```
HealthAssistant/
├── app.py
├── main.py
├── run.py
├── routes.py
├── models.py
├── forms.py
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── test.css
│   └── js/
│       └── main.js
└── templates/
    ├── base.html
    ├── index.html
    └── ...
```

### 7. Environment Setup

Make sure you have the required dependencies:
```bash
pip install -r requirements.txt
```

### 8. Debug Information

The app includes debug routes to help troubleshoot:
- `/debug-static` - Shows static file paths and existence
- `/test-css` - Tests CSS loading
- `/test` - Tests static file serving

### 9. Force Refresh

If you're still having issues:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh the page (Ctrl+F5)
3. Try in incognito/private browsing mode
4. Check if the issue persists in different browsers

### 10. Alternative Solutions

If static files still don't work:
1. Check if your firewall/antivirus is blocking localhost
2. Try running on a different port
3. Check if another application is using port 5000
4. Verify Python and Flask versions are compatible
