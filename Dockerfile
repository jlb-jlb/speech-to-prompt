FROM python:3.13-slim

# 1. Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Install uv (Best Practice: Copy binary) [file:1]
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# 3. Configure environment
# Compile bytecode for faster startup [file:1]
ENV UV_COMPILE_BYTECODE=1 
# Use copy mode for cache stability in Docker [file:1]
ENV UV_LINK_MODE=copy 
# Add the venv to PATH so you can just run "python" or "uv run" directly
ENV PATH="/app/.venv/bin:$PATH"

# 4. Install Dependencies (Cached Layer)
# We use bind mounts for the config files so we don't need to COPY them yet.
# --no-install-project installs dependencies but SKIPS your own code/readme.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# 5. Copy Source Code & Project Metadata
# Now we copy the files needed for the final app install
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

# 6. Install Project (Fast Layer)
# This only installs your specific "speech-to-prompt" package.
# Since dependencies are already there, this takes milliseconds.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# 7. Run
EXPOSE 7860
# Because we added .venv/bin to PATH, we can run the module directly
CMD ["python", "-m", "speech_to_prompt.main"]
