from pydub import AudioSegment
from transformers import pipeline
import whisper
# Convert audio to WAV for uniform processing
def convert_to_wav(upload_path):
    audio = AudioSegment.from_file(upload_path)
    wav_path = upload_path.rsplit('.', 1)[0] + ".wav"
    audio.export(wav_path, format="wav")
    return wav_path

# model = whisper.load_model("base")

# def transcribe_audio(audio_path):
#     print("🔍 Transcribing with Whisper...")
#     result = model.transcribe(audio_path)
#     return result["text"]

# # Summarization using Hugging Face
# summarizer = pipeline("summarization")

# def summarize_text(text):
#     return summarizer(text, max_length=100, min_length=25, do_sample=False)[0]['summary_text']

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

def summarize_text(text):
    prompt = f"Summarize the following transcript:\n\n{text}"
    response = model.generate_content(prompt)
    print("🧠 Gemini response (raw):", response)
    return response.text.strip()
