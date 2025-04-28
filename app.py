# from flask import Flask, request, jsonify, session 
# from processor import convert_to_wav, transcribe_audio, summarize_text
# from utils.qa_module import answer_question
# import os
# from werkzeug.security import generate_password_hash, check_password_hash
# import sqlite3

# # Setup database
# def init_db():
#     with sqlite3.connect("users.db") as conn:
#         conn.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 email TEXT UNIQUE NOT NULL,
#                 password TEXT NOT NULL
#             )
#         """)
# init_db()



# app = Flask(__name__)
# UPLOAD_FOLDER = "static/uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route("/")
# def home():
#     return "Transcripto API is live 🚀"

# @app.route("/signup", methods=["POST"])
# def signup():
#     data = request.json
#     email = data.get("email")
#     password = data.get("password")
#     name = data.get("name")
#     if not email or not password or not name:
#         return jsonify({"error": "Name, email, and password required"}), 400
    
#     hashed = generate_password_hash(password)
#     try:
#         with sqlite3.connect("users.db") as conn:
#             conn.execute("INSERT INTO users (email, name, password) VALUES (?, ?, ?)", (email, name, hashed))
#         return jsonify({"message": "User created successfully"}), 201
#     except sqlite3.IntegrityError:
#         return jsonify({"error": "Email already exists"}), 409

# @app.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     email = data.get("email")
#     password = data.get("password")
#     with sqlite3.connect("users.db") as conn:
#         cursor = conn.execute("SELECT name, password FROM users WHERE email = ?", (email,))
#         row = cursor.fetchone()
#         if row and check_password_hash(row[0], password):
#             jsonify({"token": email, "name": row[0]})  # Just return email as token for now
#         else:
#             return jsonify({"error": "Invalid credentials"}), 401

# @app.route("/upload", methods=["POST"])
# def upload_audio():
#     file = request.files.get("file")
#     context_type = request.form.get("context", "General Users")
#     if file is None:
#         return "No file found in request", 400

#     print(f"✅ Received file: {file.filename}")
#     filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(filepath)

#     try:
#         wav_path = convert_to_wav(filepath)
#         transcription = transcribe_audio(wav_path)
#         summary = summarize_text(transcription, context_type)
#         return jsonify({"transcript": transcription, "summary": summary})
#     except Exception as e:
#         print("🔥 Error in processing:", e)
#         return str(e), 500


# @app.route("/qa", methods=["POST"])
# def qa():
#     data = request.json
#     context_type = data.get("user_type", "General Users")
#     answer = answer_question(data["context"], data["question"], context_type)
#     return jsonify({"answer": answer})

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify, session 
from processor import convert_to_wav, transcribe_audio, summarize_text
from utils.qa_module import answer_question
import os
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# Setup database
def init_db():
    with sqlite3.connect("users.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

init_db()

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "Transcripto API is live 🚀"

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if not email or not password or not name:
        return jsonify({"error": "Name, email, and password required"}), 400
    
    hashed = generate_password_hash(password)
    try:
        with sqlite3.connect("users.db") as conn:
            conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed))
        return jsonify({"message": "User created successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    with sqlite3.connect("users.db") as conn:
        cursor = conn.execute("SELECT name, password FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row and check_password_hash(row[1], password):
            return jsonify({"token": email, "name": row[0]})
        else:
            return jsonify({"error": "Invalid credentials"}), 401

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
