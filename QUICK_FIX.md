# 🚀 Quick Fix for Styling Issues - PowerShell Edition

## The Problem
You're seeing plain HTML without styling when running the Flask app in PowerShell.

## 🔧 Step-by-Step Solution

### Step 1: Install Dependencies
Open PowerShell and run:
```powershell
pip install -r requirements.txt
```

### Step 2: Run the Flask App (Choose ONE method)

**Method A: Use the run script (Recommended)**
```powershell
python run.py
```

**Method B: Use main.py**
```powershell
python main.py
```

**Method C: Use Flask CLI**
```powershell
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
flask run
```

### Step 3: Test the App
1. Open your browser
2. Go to: `http://localhost:5000`
3. You should see a styled page with:
   - Blue navigation bar
   - Styled buttons
   - Cards with shadows
   - Proper typography

### Step 4: If Still No Styling

**Test 1: Check static files**
Visit: `http://localhost:5000/debug-static`
This will show if static files exist and their paths.

**Test 2: Try simple CSS test**
Visit: `http://localhost:5000/test-simple`
This should show styled content.

**Test 3: Force refresh browser**
Press `Ctrl + F5` to clear cache and force refresh.

## 🐛 Common Issues & Solutions

### Issue: "No module named 'flask'"
**Solution:**
```powershell
pip install flask flask-login flask-sqlalchemy flask-wtf
```

### Issue: "Address already in use"
**Solution:**
```powershell
# Kill existing process
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

### Issue: Still no styling
**Solution:**
1. Open browser Developer Tools (F12)
2. Go to Network tab
3. Refresh page
4. Look for failed CSS requests
5. Check Console for errors

## 🧪 Test Scripts

If the main app still doesn't work, try these test scripts:

**Test 1: Static file test**
```powershell
python test_flask.py
```
Then visit: `http://localhost:5001`

**Test 2: Template test**
```powershell
python test_template.py
```
Then visit: `http://localhost:5002`

## ✅ Success Indicators

You'll know it's working when you see:
- ✅ Blue navigation bar with white background
- ✅ Styled buttons with hover effects
- ✅ Cards with shadows and rounded corners
- ✅ Responsive layout
- ✅ Proper typography and spacing

## 🔍 Debug Steps

1. **Check if Flask is running:**
   - You should see "Running on http://0.0.0.0:5000" in terminal

2. **Check static file configuration:**
   - Visit `http://localhost:5000/debug-static`
   - Should show static files exist

3. **Check browser console:**
   - Press F12 in browser
   - Look for any red error messages

4. **Try different browser:**
   - Test in Chrome, Firefox, or Edge
   - Try incognito/private mode

## 🆘 Still Not Working?

If you're still having issues:

1. **Check file structure:**
   ```
   HealthAssistant/
   ├── static/
   │   ├── css/
   │   │   └── style.css
   │   └── js/
   │       └── main.js
   ├── templates/
   │   ├── base.html
   │   └── index.html
   ├── app.py
   ├── main.py
   └── run.py
   ```

2. **Verify Python version:**
   ```powershell
   python --version
   ```

3. **Check Flask installation:**
   ```powershell
   python -c "import flask; print(flask.__version__)"
   ```

4. **Try running on different port:**
   Edit `run.py` and change port from 5000 to 8000

## 📞 Need More Help?

If none of these solutions work, please share:
1. The exact error messages you see
2. What happens when you visit the debug URLs
3. Your Python and Flask versions
4. Screenshots of the unstyled page
