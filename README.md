# Transcripto

An end-to-end application for audio transcription, summarization, and Q&A — with authentication!
Built using **Flet** (for frontend) + **Flask** (for backend) + **Whisper**, **Gemini**, and **HuggingFace** pipelines.

---

## Features

- User Authentication (Signup/Login)
- Upload audio files (any format)
- Transcription using OpenAI Whisper
- Summarization using Gemini 2.0
- Interactive Q&A using Huggingface transformers
- Simple, beautiful UI built with Flet

---

## Project Structure

```
transcripto/
├── app.py          # Flask Backend API
├── processor.py    # Audio Processing, Transcription, Summarization
├── ui.py           # Flet Frontend App
├── utils/
│   └── qa_module.py # QA module using Huggingface pipeline
├── static/uploads/ # Uploaded audio files (runtime)
├── users.db        # SQLite Database (runtime)
├── README.md       # Project README
└── requirements.txt# Dependencies
```

---

## Linked Files

- [app.py](./app.py) → Flask API (authentication, file upload, QA endpoints)
- [ui.py](./ui.py) → Flet UI frontend
- [processor.py](./processor.py) → Audio to text, summarization
- [utils/qa_module.py](./utils/qa_module.py) → Q&A model using Huggingface

---

## Requirements

- Python 3.8+
- [Flet](https://flet.dev/)
- [Flask](https://flask.palletsprojects.com/)
- [pydub](https://github.com/jiaaro/pydub)
- [openai-whisper](https://github.com/openai/whisper)
- [transformers](https://huggingface.co/docs/transformers/index)
- [google-generativeai](https://github.com/google/generative-ai-python)
- SQLite3 (comes built-in with Python)

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/transcripto.git
cd transcripto
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Setup Environment Variables**

Create a `.env` file with your Gemini API key:

```env
GOOGLE_API_KEY=your-gemini-api-key-here
```

5. **Run Backend Server**

```bash
python app.py
```

6. **Run Frontend UI**

In another terminal:

```bash
python ui.py
```

---

## Usage

- Sign up or log in.
- Upload an audio file (mp3, wav, etc.).
- View the transcript and summary.
- Ask questions about the transcript and get instant answers!

---

## Technologies Used

- **Flet** — Flutter-like apps in Python
- **Flask** — Python backend API
- **Whisper** — Speech-to-Text by OpenAI
- **Gemini 2.0** — Text Summarization
- **HuggingFace Transformers** — QA Module
- **SQLite** — Lightweight user database

---

## Future Improvements

- Multi-file uploads
- Role-based dashboards (student/business/journalist)
- Save transcripts and Q&A history
- Dockerize the whole project

---

## License

This project is licensed under the MIT License.

