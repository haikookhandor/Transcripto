import flet as ft
import requests

BACKEND_URL = "http://127.0.0.1:5000"

def upload_file(page: ft.Page, e: ft.FilePickerResultEvent):
    if not e.files:
        page.snack_bar = ft.SnackBar(content=ft.Text("No file selected."))
        page.snack_bar.open = True
        page.update()
        return

    file_path = e.files[0].path

    with open(file_path, "rb") as f:
        response = requests.post(f"{BACKEND_URL}/upload", files={"file": f})

    if response.status_code == 200:
        data = response.json()
        page.controls[2].value = data.get("transcription", "Error in transcription")  # transcription
        page.controls[4].value = data.get("summary", "Error in summarization")  # summary
    else:
        page.controls[2].value = "Upload failed."

    page.update()

def ask_question(page: ft.Page, e):
    text = page.controls[2].value  # transcription
    query = page.controls[5].value  # question_input

    response = requests.post(f"{BACKEND_URL}/ask", json={"text": text, "query": query})
    if response.status_code == 200:
        page.controls[7].value = response.json().get("answer", "Error in Q&A")  # answer
    else:
        page.controls[7].value = "Error in request."

    page.update()

def main(page: ft.Page):
    page.title = "Transcripto"

    file_picker = ft.FilePicker(on_result=lambda e: upload_file(page, e))
    page.overlay.append(file_picker)

    upload_button = ft.ElevatedButton("Upload Audio", on_click=lambda e: file_picker.pick_files(allow_multiple=False))
    result = ft.Text("Select a file to upload.")
    transcription = ft.Text("", selectable=True)
    summary = ft.Text("", selectable=True)

    question_input = ft.TextField(label="Ask a question about the transcript")
    ask_button = ft.ElevatedButton("Ask", on_click=lambda e: ask_question(page, e))
    answer = ft.Text("", selectable=True)

    page.add(
        upload_button,
        result,
        ft.Text("Transcription:"), transcription,
        ft.Text("Summary:"), summary,
        question_input, ask_button,
        ft.Text("Answer:"), answer
    )

ft.app(target=main)
