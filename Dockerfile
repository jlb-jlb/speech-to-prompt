# Use NVIDIA's official CUDA runtime image (includes cuDNN)
# This is REQUIRED for CTranslate2/Faster-Whisper to use the GPU
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# 1. Install Python and FFmpeg
# Since we are on Ubuntu now (not python-slim), we install python3 manually
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    python3-pip \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Install uv (Best Practice: Copy binary)
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# 3. Configure environment
ENV UV_COMPILE_BYTECODE=1 
ENV UV_LINK_MODE=copy 
# Ensure we use the system python or venv correctly
ENV PATH="/app/.venv/bin:$PATH"

# 4. Install Dependencies (Cached Layer)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --python-preference only-system

# 5. Copy Source Code
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

# 6. Install Project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --python-preference only-system

RUN ldconfig /usr/local/cuda/lib64
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64

# 7. Run
EXPOSE 7860
CMD ["python3", "-m", "speech_to_prompt.main"]
