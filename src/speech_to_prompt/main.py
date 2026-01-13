import gradio as gr
from faster_whisper import WhisperModel
import os
from openai import OpenAI
import ollama

# --- Configuration ---
# Choose model size: "tiny", "base", "small", "medium", "large-v3"
STT_MODEL_SIZE = "base"
# Use "cuda" if your Docker container has GPU access, otherwise "cpu"
device = (
    "cuda"
    if os.environ.get("CUDA_VISIBLE_DEVICES")
    or os.environ.get("NVIDIA_VISIBLE_DEVICES")
    else "cpu"
)

print(f"Initializing Service on device: {device}")
print(f"Loading Whisper {STT_MODEL_SIZE} model...")

# Initialize Whisper once (faster than reloading)
try:
    model = WhisperModel(STT_MODEL_SIZE, device=device, compute_type="int8")
except Exception as e:
    print(f"Warning: Failed to load on {device}, falling back to CPU. Error: {e}")
    model = WhisperModel(STT_MODEL_SIZE, device="cpu", compute_type="int8")


def speech_to_prompt(audio_path, llm_choice, api_key):
    """
    1. Transcribes audio file using Faster-Whisper.
    2. Sends text to LLM (Ollama or OpenAI) for refinement.
    """
    if audio_path is None:
        return "No audio recorded.", "Please record audio first."

    # --- Step 1: Transcribe (Speech to Text) ---
    print(f"Transcribing audio file: {audio_path}")
    try:
        segments, info = model.transcribe(audio_path, beam_size=5)
        transcribed_text = " ".join([segment.text for segment in segments])
        print("Transcription complete.")
    except Exception as e:
        return f"Error during transcription: {str(e)}", "Consult container logs."

    # --- Step 2: Refine (Text to Prompt) ---
    system_instruction = (
        "You are a Prompt Engineer. The user will provide a raw spoken transcript "
        "that is messy, contains filler words, may be rambling and may have speech to text artifacts."
        "Your goal is to convert this into a clear, concise, and effective prompt "
        "You must assume, that the User and the Chatbot already have a conversation history, so you may not know exactly, what the user is talking about."
        "optimized for an LLM chatbot. Output ONLY the optimized prompt."
    )

    refined_prompt = ""

    try:
        if llm_choice == "Local (Ollama)":
            print("Sending to Ollama (gemma-3)...")

            # Ollama Python client automatically checks OLLAMA_HOST env var
            # If running in Docker without --net=host, ensure -e OLLAMA_HOST is set
            response = ollama.chat(
                model="gemma3",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": transcribed_text},
                ],
            )
            refined_prompt = response["message"]["content"]

        elif llm_choice == "Cloud (OpenAI)":
            print("Sending to OpenAI (gpt-4o-mini)...")
            if not api_key:
                return (
                    transcribed_text,
                    "Error: Please provide an OpenAI API Key in the settings.",
                )

            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Cheap, fast model
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": transcribed_text},
                ],
            )
            refined_prompt = response.choices[0].message.content

    except Exception as e:
        error_msg = str(e)
        print(f"LLM Error: {error_msg}")
        if "Connection refused" in error_msg and llm_choice == "Local (Ollama)":
            refined_prompt = (
                f"Error: Could not connect to Ollama.\n\n"
                f"1. Is Ollama running? (Check 'ollama serve')\n"
                f"2. If in Docker, did you set OLLAMA_HOST?\n"
                f"   (e.g., -e OLLAMA_HOST=http://host.docker.internal:11434)\n"
                f"Original Error: {error_msg}"
            )
        else:
            refined_prompt = f"Error processing with LLM: {error_msg}"

    return transcribed_text, refined_prompt


# --- GUI Layout ---
def create_interface():
    with gr.Blocks(title="Speech to Prompt") as demo:
        gr.Markdown("# 🎙️ Speech to Prompt Converter")
        gr.Markdown("Record your messy thoughts, get a clean AI prompt.")

        with gr.Row():
            with gr.Column(scale=1):
                # The Audio component handles Play (Record), Pause, and Stop natively in browser
                audio_input = gr.Audio(
                    sources=["microphone"], type="filepath", label="Record Command"
                )

                with gr.Accordion("⚙️ Settings", open=True):
                    llm_selector = gr.Radio(
                        ["Local (Ollama)", "Cloud (OpenAI)"],
                        label="Processing Model",
                        value="Local (Ollama)",
                    )
                    api_key_input = gr.Textbox(
                        label="OpenAI API Key (Required only for Cloud)",
                        type="password",
                        placeholder="sk-...",
                    )

                convert_btn = gr.Button(
                    "🚀 Convert to Prompt", variant="primary", size="lg"
                )

            with gr.Column(scale=1):
                transcript_output = gr.TextArea(
                    label="Raw Transcription", lines=4, interactive=False
                )
                # Change gr.TextArea to gr.Textbox
                prompt_output = gr.Textbox(
                    label="Optimized Prompt",
                    lines=4,
                    # show_copy_button=True, # This works on Textbox in Gradio 4+
                    interactive=False
                )


        # Event wiring
        convert_btn.click(
            fn=speech_to_prompt,
            inputs=[audio_input, llm_selector, api_key_input],
            outputs=[transcript_output, prompt_output],
        )

    return demo


def main():
    demo = create_interface()
    print("Starting Gradio Server on port 7860...")
    # server_name="0.0.0.0" is crucial for Docker to expose the port
    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
