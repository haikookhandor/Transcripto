from pydub import AudioSegment
from transformers import pipeline
import whisper
# Convert audio to WAV for uniform processing
def convert_to_wav(upload_path):
    audio = AudioSegment.from_file(upload_path)
    wav_path = upload_path.rsplit('.', 1)[0] + ".wav"
    audio.export(wav_path, format="wav")
    return wav_path

# # Placeholder for Gemini 2.0 transcription
# def transcribe_audio(audio_path):
#     # Simulate transcription
#     return "This is the transcribed text of the uploaded audio."


model = whisper.load_model("base")

def transcribe_audio(audio_path):
    print("🔍 Transcribing with Whisper...")
    result = model.transcribe(audio_path)
    return result["text"]

# Summarization using Hugging Face
summarizer = pipeline("summarization")

def summarize_text(text):
    return summarizer(text, max_length=100, min_length=25, do_sample=False)[0]['summary_text']
