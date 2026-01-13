#!/usr/bin/env python3
"""
Simple installation test to verify all dependencies are working.
"""

def test_imports():
    """Test that all required packages can be imported."""
    print("🧪 Testing package imports...")
    
    try:
        import gradio as gr
        print("✅ gradio imported successfully")
    except ImportError as e:
        print(f"❌ gradio import failed: {e}")
        return False
    
    try:
        from faster_whisper import WhisperModel
        print("✅ faster-whisper imported successfully")
    except ImportError as e:
        print(f"❌ faster-whisper import failed: {e}")
        return False
    
    try:
        import ollama
        print("✅ ollama imported successfully")
    except ImportError as e:
        print(f"❌ ollama import failed: {e}")
        return False
    
    try:
        from openai import OpenAI
        print("✅ openai imported successfully")
    except ImportError as e:
        print(f"❌ openai import failed: {e}")
        return False
    
    try:
        from src.speech_to_prompt import main
        print("✅ speech_to_prompt package imported successfully")
    except ImportError as e:
        print(f"❌ speech_to_prompt import failed: {e}")
        return False
    
    return True

def test_whisper_model():
    """Test that Whisper model can be initialized (without downloading)."""
    print("\n🎯 Testing Whisper model initialization...")
    try:
        from faster_whisper import WhisperModel
        # This will only test the class, not download the model
        print("✅ WhisperModel class available")
        return True
    except Exception as e:
        print(f"❌ WhisperModel test failed: {e}")
        return False

def main():
    print("🚀 Speech to Prompt - Installation Test")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test Whisper
    if not test_whisper_model():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Your installation is ready.")
        print("💡 Run 'uv run speech-to-prompt' or 'python dev.py' to start the app.")
    else:
        print("❌ Some tests failed. Please check your installation.")
        print("💡 Try running 'uv sync' to reinstall dependencies.")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())