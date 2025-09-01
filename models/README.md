# 🤖 AI Models for Health Assistant

This folder contains AI models and integration code for enhanced medical text analysis.

## 📁 Contents

- **`huggingface_integration.py`** - Main integration module for Hugging Face models
- **`download_model.py`** - Script to download and set up models
- **`requirements.txt`** - Dependencies for AI model functionality
- **`medical_text_classifier/`** - Downloaded model files (created after running download script)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r models/requirements.txt
```

### 2. Download Model
```bash
cd models
python download_model.py
```

### 3. Use in Your Application
```python
from models.huggingface_integration import analyze_symptoms_with_model

# Analyze symptoms
result = analyze_symptoms_with_model("I have a fever and headache")
print(result)
```

## 🔧 Features

- **Automatic Fallback**: If models aren't available, falls back to basic analysis
- **Lightweight**: Uses small, efficient models to avoid performance issues
- **Medical Focus**: Optimized for health-related text analysis
- **Easy Integration**: Simple API that works with existing code

## 📊 Model Capabilities

### With AI Model:
- Advanced symptom analysis
- Condition prediction
- Treatment recommendations
- Confidence scoring

### Fallback Mode:
- Basic symptom detection
- Simple condition mapping
- General health advice
- Reliable performance

## ⚠️ Important Notes

- Models are downloaded locally to avoid internet dependency
- Fallback mode ensures the app always works
- Models are lightweight to avoid memory issues
- No sensitive data is sent to external services

## 🆘 Troubleshooting

If you encounter issues:

1. **Check dependencies**: Ensure all packages are installed
2. **Verify model files**: Check if `medical_text_classifier/` folder exists
3. **Check logs**: Look for error messages in the console
4. **Fallback mode**: The app will work even without models

## 🔄 Updating Models

To update or change models:

1. Delete the `medical_text_classifier/` folder
2. Run `python download_model.py` again
3. The new model will be downloaded automatically

## 📝 License

Models are used according to their respective licenses. Check individual model documentation for details.
