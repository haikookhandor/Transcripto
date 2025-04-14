from flask import Flask, request, jsonify
from processor import convert_to_wav, transcribe_audio, summarize_text
from utils.qa_module import answer_question
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "Transcripto API is live 🚀"

@app.route("/upload", methods=["POST"])
def upload_audio():
    file = request.files.get("file")
    context_type = request.form.get("context", "General Users")
    if file is None:
        return "No file found in request", 400

    print(f"✅ Received file: {file.filename}")
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        wav_path = convert_to_wav(filepath)
        transcription = transcribe_audio(wav_path)
        summary = summarize_text(transcription, context_type)
        return jsonify({"transcript": transcription, "summary": summary})
    except Exception as e:
        print("🔥 Error in processing:", e)
        return str(e), 500


@app.route("/qa", methods=["POST"])
def qa():
    data = request.json
    context_type = data.get("user_type", "General Users")
    answer = answer_question(data["context"], data["question"], context_type)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)

