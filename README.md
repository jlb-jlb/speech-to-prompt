# Speech to Prompt

A web-based application that converts speech to optimized prompts for LLM chatbots. Record your voice, get a transcription, and have it refined into a clear, effective prompt.

## Features

- 🎙️ **Browser-based recording** - No complex microphone setup needed
- 🚀 **Fast transcription** - Uses Faster-Whisper for efficient speech-to-text
- 🤖 **Dual LLM support** - Choose between local Ollama or cloud OpenAI
- 🐳 **Docker ready** - Easy containerized deployment
- 📝 **Copy-friendly output** - One-click copy of optimized prompts

## Architecture

1. **Record** - Browser handles microphone access and recording
2. **Transcribe** - Faster-Whisper converts speech to text
3. **Refine** - LLM (Ollama/OpenAI) optimizes the transcript into a clear prompt

## Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Run the application**:
   ```bash
   uv run speech-to-prompt
   # or
   python run.py
   ```

3. **Open your browser** to `http://localhost:7860`

### Docker Deployment

1. **Build the image**:
   ```bash
   docker build -t speech-to-prompt .
   ```

2. **Run the container**:
   ```bash
   # For local Ollama access
   docker run -it --net=host -p 7860:7860 speech-to-prompt
   
   # Or with port mapping only
   docker run -it -p 7860:7860 speech-to-prompt
   ```

## Usage

1. Open `http://localhost:7860` in your browser
2. Click the microphone icon to start recording
3. Speak your prompt (can be messy, with filler words)
4. Click stop when finished
5. Choose your processing model (Local Ollama or Cloud OpenAI)
6. If using OpenAI, enter your API key
7. Click "🚀 Convert to Prompt"
8. Copy the optimized prompt from the output area

## Configuration

### Local LLM (Ollama)

For local processing, ensure Ollama is running:

```bash
# Install and start Ollama
ollama pull llama3
ollama serve
```

### Cloud LLM (OpenAI)

For cloud processing, you'll need an OpenAI API key. The app uses the cost-effective `gpt-4o-mini` model.

## Dependencies

- **gradio** - Web interface
- **faster-whisper** - Efficient speech transcription
- **ollama** - Local LLM client
- **openai** - OpenAI API client

## Development

The project uses `uv` for dependency management and follows a standard Python package structure:

```
src/speech_to_prompt/
├── __init__.py
└── main.py
```

## Docker Notes

- The container exposes port 7860
- Uses `--net=host` for easy Ollama access on the host machine
- Includes ffmpeg for audio processing
- Based on Python 3.13 slim image for efficiency