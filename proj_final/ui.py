import flet as ft
import requests

API_UPLOAD = "http://127.0.0.1:5000/upload"
API_QA = "http://127.0.0.1:5000/qa"

def main(page: ft.Page):
    page.title = "Transcripto"
    output = ft.Text(value="")
    summary = ft.Text(value="")
    answer = ft.Text(value="")
    
    def upload_file(e):
        file = file_picker.result.files[0]
        with open(file.path, "rb") as f:
            files = {"file": f}
            res = requests.post(API_UPLOAD, files=files).json()
            output.value = "Transcript:\n" + res["transcript"]
            summary.value = "Summary:\n" + res["summary"]
            page.update()
    
    def ask_question(e):
        q = question_field.value
        res = requests.post(API_QA, json={
            "context": output.value.replace("Transcript:\n", ""),
            "question": q
        }).json()
        answer.value = "Answer: " + res["answer"]
        page.update()
    
    file_picker = ft.FilePicker(on_result=upload_file)
    page.overlay.append(file_picker)

    question_field = ft.TextField(label="Ask a question")
    ask_button = ft.ElevatedButton("Ask", on_click=ask_question)

    page.add(
        ft.Row([ft.ElevatedButton("Upload Audio", on_click=lambda e: file_picker.pick_files()), question_field, ask_button]),
        output,
        summary,
        answer
    )

ft.app(target=main)
