# Speech to Prompt

A web-based application that converts messy speech recordings into clean, optimized prompts for LLM chatbots. Perfect for when you have a complex idea but struggle to articulate it clearly in text.

## Features

- **Browser-based Recording**: Record directly in your browser with play/pause/stop controls
- **Fast Transcription**: Uses Faster-Whisper for efficient speech-to-text conversion
- **AI-Powered Refinement**: Transforms rambling speech into clear, concise prompts
- **Dual LLM Support**: Choose between local (Ollama) or cloud (OpenAI) processing
- **Docker Ready**: Fully containerized with GPU support for optimal performance
- **Hot Reload**: Development mode with live code updates

## How It Works

1. **Record**: Speak your thoughts naturally using the web interface
2. **Transcribe**: Faster-Whisper converts your speech to text
3. **Refine**: An LLM transforms the raw transcript into a polished prompt
4. **Copy**: Use the optimized prompt in your favorite AI chatbot

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/jlb-jlb/speech-to-prompt.git
cd speech-to-prompt

# Build and run with Docker Compose
docker compose up --build

# Access the app at http://localhost:7860
```

### Option 2: Local Development

```bash
# Install dependencies with uv
uv sync

# Test installation
uv run python test_install.py

# Run in development mode
uv run python dev.py

# Or use the package entry point
uv run speech-to-prompt
```

## Requirements

### System Requirements
- Python 3.12+
- FFmpeg (for audio processing)
- CUDA-compatible GPU (optional, for faster processing)

### LLM Backend (Choose One)
- **Local**: [Ollama](https://ollama.ai/) with Gemma 3 model
- **Cloud**: OpenAI API key

## Configuration

### Local LLM Setup (Ollama)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the Gemma 3 model
ollama pull gemma3

# Start Ollama server
ollama serve
```

### Docker with GPU Support
The application automatically detects and uses CUDA if available. The Docker setup includes:
- NVIDIA GPU support
- CUDA runtime environment
- Optimized memory usage

### Environment Variables
- `OLLAMA_HOST`: Ollama server URL (default: `http://host.docker.internal:11434`)
- `CUDA_VISIBLE_DEVICES`: GPU device selection
- `GRADIO_SERVER_NAME`: Server bind address

## Usage

1. **Open the Web Interface**: Navigate to `http://localhost:7860`
2. **Choose Your LLM**: Select between Local (Ollama) or Cloud (OpenAI)
3. **Configure API Key**: If using OpenAI, enter your API key in settings
4. **Record Audio**: Click the microphone icon and speak naturally
5. **Convert**: Click "Convert to Prompt" to process your recording
6. **Copy Result**: Use the optimized prompt in your AI conversations

## Project Structure

```
speech-to-prompt/
├── src/speech_to_prompt/
│   ├── __init__.py
│   └── main.py              # Core application logic
├── compose.yaml             # Docker Compose configuration
├── Dockerfile               # Container build instructions
├── pyproject.toml          # Project dependencies and metadata
├── dev.py                  # Development server runner
├── test_install.py         # Installation verification
└── README.md               # This file
```

## Development

### Running Tests
```bash
# Verify installation
uv run python test_install.py
```

### Development Mode
```bash
# Start with hot reload and debug mode
uv run python dev.py

# Or use the package entry point
uv run speech-to-prompt

# Or use Gradio's built-in reload
uv run gradio src/speech_to_prompt/main.py
```

### Docker Development
```bash
# Build and run with file watching
docker compose watch

# View logs
docker compose logs -f app
```

## Model Configuration

### Whisper Model Sizes
- `tiny`: Fastest, least accurate (~39 MB)
- `base`: Good balance (~74 MB) - **Default**
- `small`: Better accuracy (~244 MB)
- `medium`: High accuracy (~769 MB)
- `large-v3`: Best accuracy (~1550 MB)

Edit `STT_MODEL_SIZE` in `src/speech_to_prompt/main.py` to change the model.

### LLM Models
- **Ollama**: Gemma 3 (default), Llama 3, Mistral, etc.
- **OpenAI**: GPT-4o-mini (default), GPT-4, GPT-3.5-turbo

## Troubleshooting

### Common Issues

**"Could not connect to Ollama"**
- Ensure Ollama is running: `ollama serve`
- Check the model is installed: `ollama list`
- Verify Docker networking if using containers

**"No audio recorded"**
- Check browser microphone permissions
- Ensure you're using HTTPS or localhost
- Try a different browser

**GPU not detected**
- Install NVIDIA Docker runtime
- Verify CUDA installation: `nvidia-smi`
- Check Docker GPU access: `docker run --gpus all nvidia/cuda:12.2.2-base-ubuntu22.04 nvidia-smi`

**Import errors**
- Run installation test: `uv run python test_install.py`
- Reinstall dependencies: `uv sync --reinstall`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

**jlb-jlb** - [joscha.bisping@gmail.com](mailto:joscha.bisping@gmail.com)

---

*Transform your messy thoughts into perfect prompts with Speech to Prompt!*