#!/usr/bin/env python3
"""
Test script for Hugging Face model integration
"""

import sys
import os

# Add models directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

def test_model_integration():
    """Test the model integration"""
    print("🧪 Testing Hugging Face Model Integration")
    print("=" * 50)
    
    try:
        # Import the model integration
        from huggingface_integration import analyze_symptoms_with_model, get_model_status
        
        print("✅ Successfully imported model integration")
        
        # Get model status
        status = get_model_status()
        print(f"📊 Model Status: {status['model_type']}")
        print(f"🔧 Model Loaded: {status['model_loaded']}")
        print(f"📁 Model Path: {status['model_path']}")
        
        # Test symptom analysis
        test_cases = [
            "I have a fever and headache",
            "My throat is sore and I'm coughing",
            "I feel tired and have muscle pain"
        ]
        
        print("\n🔍 Testing Symptom Analysis:")
        for i, symptoms in enumerate(test_cases, 1):
            print(f"\nTest {i}: {symptoms}")
            result = analyze_symptoms_with_model(symptoms)
            print(f"  Analysis: {result['analysis']}")
            print(f"  Confidence: {result['confidence']:.2%}")
            
            if 'symptoms_detected' in result:
                print(f"  Symptoms: {', '.join(result['symptoms_detected'])}")
            
            if 'potential_conditions' in result:
                print(f"  Conditions: {', '.join(result['potential_conditions'])}")
        
        print("\n✨ All tests completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure you're in the correct directory and models are set up")
        return False
        
    except Exception as e:
        print(f"❌ Test Error: {e}")
        print(f"📝 Error details: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_model_integration()
    
    if success:
        print("\n🎉 Model integration is working correctly!")
        print("🚀 Your Health Assistant is ready to use AI-powered analysis!")
    else:
        print("\n⚠️  Model integration has issues.")
        print("🔧 Check the error messages above and ensure models are properly set up.")
    
    print("\n" + "=" * 50)
    print("🏥 Health Assistant Model Test Complete")
