from flask import Flask, request, jsonify
from pydub import AudioSegment
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set your Gemini API key
GEMINI_API_KEY = "AIzaSyA1U2MNa2EzpMGxGNdBo7aJg6p4W9xLWYs"
GEMINI_TRANSCRIBE_URL = "https://api.gemini.com/v1/audio/transcribe"
GEMINI_SUMMARIZE_URL = "https://api.gemini.com/v1/text/summarize"
GEMINI_QA_URL = "https://api.gemini.com/v1/text/qa"

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        response = requests.post(
            GEMINI_TRANSCRIBE_URL,
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
            files={"file": audio_file}
        )
    
    if response.status_code == 200:
        return response.json().get("transcription", "Error in transcription")
    else:
        return "Error: " + response.text

def summarize_text(text):
    response = requests.post(
        GEMINI_SUMMARIZE_URL,
        headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
        json={"text": text}
    )
    
    if response.status_code == 200:
        return response.json().get("summary", "Error in summarization")
    else:
        return "Error: " + response.text

def answer_query(text, query):
    response = requests.post(
        GEMINI_QA_URL,
        headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
        json={"text": text, "query": query}
    )
    
    if response.status_code == 200:
        return response.json().get("answer", "Error in Q&A")
    else:
        return "Error: " + response.text

@app.route("/upload", methods=["POST"])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    transcription = transcribe_audio(file_path)
    summary = summarize_text(transcription)
    
    return jsonify({"transcription": transcription, "summary": summary})

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.json
    text = data.get("text", "")
    query = data.get("query", "")
    
    answer = answer_query(text, query)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
