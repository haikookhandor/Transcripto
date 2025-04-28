from pydub import AudioSegment
from transformers import pipeline
import whisper
# Convert audio to WAV for uniform processing
def convert_to_wav(upload_path):
    audio = AudioSegment.from_file(upload_path)
    wav_path = upload_path.rsplit('.', 1)[0] + ".wav"
    audio.export(wav_path, format="wav")
    return wav_path

import google.generativeai as genai
import os

# Initialize Gemini
genai.configure(api_key=os.getenv("AIzaSyA1U2MNa2EzpMGxGNdBo7aJg6p4W9xLWYs"))

model = genai.GenerativeModel("gemini-2.0-flash")

def transcribe_audio(audio_path):
    # ✅ Step 1: Convert audio to text prompt using Whisper first (or upload to Google Cloud Storage for Gemini Audio support later)
    import whisper
    whisper_model = whisper.load_model("base")
    result = whisper_model.transcribe(audio_path)
    transcript = result["text"]
    return transcript

def summarize_text(text, context_type="General Users"):
    prompt = f"You are summarizing for a user type: {context_type}. Summarize this transcript accordingly:\n\n{text}"
    response = model.generate_content(prompt)
    print("🧠 Gemini response (raw):", response)
    return response.text.strip()
