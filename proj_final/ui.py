import flet as ft
import requests

API_UPLOAD = "http://127.0.0.1:5000/upload"
API_QA = "http://127.0.0.1:5000/qa"

def main(page: ft.Page):
    page.title = "🎙️ Transcripto"
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    selected_user_type = {"value": "General Users"}
    status_text = ft.Text(value="🎯 Selected: General Users", size=16, color=ft.colors.BLUE_600)
    transcript_output = ft.Text(value="", selectable=True)
    summary_output = ft.Text(value="", selectable=True)
    qa_column = ft.Column(spacing=10)
    question_field = ft.TextField(label="Ask a question", expand=True)
    ask_button = ft.ElevatedButton("Ask", on_click=lambda e: None)  # Dummy init

    # User type buttons (we’ll update these on selection)
    user_type_buttons = []

    user_types = {
        "Students and Researchers": "Students",
        "Businesses and Professionals": "Business",
        "Podcasters and Journalists": "Journalists",
        "General Users": "General"
    }

    def reset_interface():
        transcript_output.value = ""
        summary_output.value = ""
        qa_column.controls.clear()
        question_field.value = ""
        status_text.value = f"🎯 Selected: {selected_user_type['value']}"
        page.update()

    def set_user_type(user_type_key):
        selected_user_type["value"] = user_type_key
        for btn in user_type_buttons:
            if btn.data == user_type_key:
                btn.style = ft.ButtonStyle(bgcolor=ft.colors.BLUE_200)
            else:
                btn.style = ft.ButtonStyle(bgcolor=ft.colors.TRANSPARENT)
        reset_interface()

    # Build the user type buttons dynamically
    user_type_row = ft.Row(
        controls=[
            ft.Text("Select User Type:", size=14)
        ] + [
            ft.ElevatedButton(
                text=label,
                on_click=lambda e, k=key: set_user_type(k),
                data=key
            ) for key, label in user_types.items()
        ],
        alignment=ft.MainAxisAlignment.START,
    )
    user_type_buttons = user_type_row.controls[1:]  # Skip the label text

    def upload_file(e):
        if not file_picker.result or not file_picker.result.files:
            status_text.value = "❌ No file selected!"
            page.update()
            return

        file = file_picker.result.files[0]
        status_text.value = "📤 Uploading and processing file..."
        page.update()

        try:
            with open(file.path, "rb") as f:
                files = {"file": f}
                data = {"context": selected_user_type["value"]}
                res = requests.post(API_UPLOAD, files=files, data=data)
                res = res.json()
                transcript_output.value = res["transcript"]
                summary_output.value = res["summary"]
                status_text.value = "✅ File processed successfully!"
        except Exception as ex:
            status_text.value = f"❌ Error: {str(ex)}"

        page.update()

    def ask_question(e):
        q = question_field.value.strip()
        if not q:
            status_text.value = "❗ Please enter a question."
            page.update()
            return

        status_text.value = "🤔 Generating answer..."
        page.update()

        try:
            response = requests.post(API_QA, json={
                "context": transcript_output.value,
                "question": q,
                "user_type": selected_user_type["value"]
            })

            if response.status_code == 200:
                try:
                    res = response.json()
                    answer = res.get("answer", "⚠️ No answer received.")
                    qa_column.controls.append(ft.Text(f"❓ Q: {q}", weight="bold"))
                    qa_column.controls.append(ft.Text(f"💡 A: {answer}"))
                    question_field.value = ""
                    status_text.value = "✅ Answer generated!"
                except ValueError:
                    status_text.value = "❌ Invalid JSON response from server."
            else:
                status_text.value = f"❌ Server error: {response.status_code}"

        except Exception as ex:
            status_text.value = f"❌ Error: {str(ex)}"

        page.update()

    file_picker = ft.FilePicker(on_result=upload_file)
    page.overlay.append(file_picker)

    ask_button.on_click = ask_question  # Assign real function now

    page.add(
        ft.Text("🎙️ Transcripto", size=32, weight="bold"),
        user_type_row,
        status_text,
        ft.ElevatedButton("Upload Audio File", icon=ft.icons.UPLOAD_FILE, on_click=lambda e: file_picker.pick_files()),
        ft.Divider(),
        ft.Text("📄 Transcript", size=20, weight="bold"),
        ft.Card(content=ft.Container(transcript_output, padding=10, bgcolor=ft.colors.GREY_100)),
        ft.Text("📝 Summary", size=20, weight="bold"),
        ft.Card(content=ft.Container(summary_output, padding=10, bgcolor=ft.colors.GREY_100)),
        ft.Divider(),
        ft.Row([question_field, ask_button]),
        ft.Text("🔎 Q&A", size=20, weight="bold"),
        ft.Card(content=ft.Container(qa_column, padding=10, bgcolor=ft.colors.GREY_100)),
    )

ft.app(target=main)

