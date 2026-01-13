#!/usr/bin/env python3
"""
Development runner with additional debugging and configuration options.
"""

import os
import sys
from src.speech_to_prompt.main import create_interface

def main():
    # Set development environment variables
    os.environ.setdefault("GRADIO_SERVER_NAME", "127.0.0.1")
    os.environ.setdefault("GRADIO_SERVER_PORT", "7860")
    
    print("🎙️ Starting Speech to Prompt in development mode...")
    print("📍 Server will be available at: http://127.0.0.1:7860")
    print("🔧 Development mode: Hot reload enabled")
    print("⚠️  Make sure you have:")
    print("   - Ollama running (if using local model): ollama serve")
    print("   - OpenAI API key (if using cloud model)")
    print()
    
    try:
        demo = create_interface()
        demo.launch(
            server_name="127.0.0.1",
            server_port=7860,
            debug=True,
            show_error=True,
            share=False
        )
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()