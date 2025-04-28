# import flet as ft
# import requests

# API_UPLOAD = "http://127.0.0.1:5000/upload"
# API_QA = "http://127.0.0.1:5000/qa"

# def main(page: ft.Page):
#     page.title = "🎙️ Transcripto"
#     page.scroll = "auto"
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.padding = 20

#     selected_user_type = {"value": "General Users"}
#     status_text = ft.Text(value="🎯 Selected: General Users", size=16, color=ft.colors.BLUE_600)
#     transcript_output = ft.Text(value="", selectable=True)
#     summary_output = ft.Text(value="", selectable=True)
#     qa_column = ft.Column(spacing=10)
#     question_field = ft.TextField(label="Ask a question", expand=True)
#     ask_button = ft.ElevatedButton("Ask", on_click=lambda e: None)  # Dummy init

#     # User type buttons (we’ll update these on selection)
#     user_type_buttons = []

#     user_types = {
#         "Students and Researchers": "Students",
#         "Businesses and Professionals": "Business",
#         "Podcasters and Journalists": "Journalists",
#         "General Users": "General"
#     }

#     def reset_interface():
#         transcript_output.value = ""
#         summary_output.value = ""
#         qa_column.controls.clear()
#         question_field.value = ""
#         status_text.value = f"🎯 Selected: {selected_user_type['value']}"
#         page.update()

#     def set_user_type(user_type_key):
#         selected_user_type["value"] = user_type_key
#         for btn in user_type_buttons:
#             if btn.data == user_type_key:
#                 btn.style = ft.ButtonStyle(bgcolor=ft.colors.BLUE_200)
#             else:
#                 btn.style = ft.ButtonStyle(bgcolor=ft.colors.TRANSPARENT)
#         reset_interface()

#     # Build the user type buttons dynamically
#     user_type_row = ft.Row(
#         controls=[
#             ft.Text("Select User Type:", size=14)
#         ] + [
#             ft.ElevatedButton(
#                 text=label,
#                 on_click=lambda e, k=key: set_user_type(k),
#                 data=key
#             ) for key, label in user_types.items()
#         ],
#         alignment=ft.MainAxisAlignment.START,
#     )
#     user_type_buttons = user_type_row.controls[1:]  # Skip the label text

#     def upload_file(e):
#         if not file_picker.result or not file_picker.result.files:
#             status_text.value = "❌ No file selected!"
#             page.update()
#             return

#         file = file_picker.result.files[0]
#         status_text.value = "📤 Uploading and processing file..."
#         page.update()

#         try:
#             with open(file.path, "rb") as f:
#                 files = {"file": f}
#                 data = {"context": selected_user_type["value"]}
#                 res = requests.post(API_UPLOAD, files=files, data=data)
#                 res = res.json()
#                 transcript_output.value = res["transcript"]
#                 summary_output.value = res["summary"]
#                 status_text.value = "✅ File processed successfully!"
#         except Exception as ex:
#             status_text.value = f"❌ Error: {str(ex)}"

#         page.update()

#     def ask_question(e):
#         q = question_field.value.strip()
#         if not q:
#             status_text.value = "❗ Please enter a question."
#             page.update()
#             return

#         status_text.value = "🤔 Generating answer..."
#         page.update()

#         try:
#             response = requests.post(API_QA, json={
#                 "context": transcript_output.value,
#                 "question": q,
#                 "user_type": selected_user_type["value"]
#             })

#             if response.status_code == 200:
#                 try:
#                     res = response.json()
#                     answer = res.get("answer", "⚠️ No answer received.")
#                     qa_column.controls.append(ft.Text(f"❓ Q: {q}", weight="bold"))
#                     qa_column.controls.append(ft.Text(f"💡 A: {answer}"))
#                     question_field.value = ""
#                     status_text.value = "✅ Answer generated!"
#                 except ValueError:
#                     status_text.value = "❌ Invalid JSON response from server."
#             else:
#                 status_text.value = f"❌ Server error: {response.status_code}"

#         except Exception as ex:
#             status_text.value = f"❌ Error: {str(ex)}"

#         page.update()

#     file_picker = ft.FilePicker(on_result=upload_file)
#     page.overlay.append(file_picker)

#     ask_button.on_click = ask_question  # Assign real function now

#     page.add(
#         ft.Text("🎙️ Transcripto", size=32, weight="bold"),
#         user_type_row,
#         status_text,
#         ft.ElevatedButton("Upload Audio File", icon=ft.icons.UPLOAD_FILE, on_click=lambda e: file_picker.pick_files()),
#         ft.Divider(),
#         ft.Text("📄 Transcript", size=20, weight="bold"),
#         ft.Card(content=ft.Container(transcript_output, padding=10, bgcolor=ft.colors.GREY_100)),
#         ft.Text("📝 Summary", size=20, weight="bold"),
#         ft.Card(content=ft.Container(summary_output, padding=10, bgcolor=ft.colors.GREY_100)),
#         ft.Divider(),
#         ft.Row([question_field, ask_button]),
#         ft.Text("🔎 Q&A", size=20, weight="bold"),
#         ft.Card(content=ft.Container(qa_column, padding=10, bgcolor=ft.colors.GREY_100)),
#     )

# ft.app(target=main)

import flet as ft
import requests

API_BASE = "http://127.0.0.1:5000"
API_LOGIN = f"{API_BASE}/login"
API_SIGNUP = f"{API_BASE}/signup"
API_UPLOAD = f"{API_BASE}/upload"
API_QA = f"{API_BASE}/qa"

def main(page: ft.Page):
    page.title = "🎙️ Transcripto Auth"
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    current_user = {"email": None, "name": None}  # Track login state
    selected_user_type = {"value": "General Users"}

    def show_login():
        page.controls.clear()

        email_field = ft.TextField(label="Email", width=300)
        password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
        login_status = ft.Text(value="")

        def do_login(e):
            res = requests.post(API_LOGIN, json={"email": email_field.value, "password": password_field.value})
            if res.status_code == 200:
                data = res.json()
                current_user["email"] = data.get("token")
                current_user["name"] = data.get("name", "User")
                show_main_ui()
            else:
                login_status.value = f"❌ {res.json().get('error', 'Login failed')}"
                page.update()

        def go_to_signup(e):
            show_signup()

        login_column = ft.Column([
            ft.Text("🔐 Login to Transcripto", size=24, weight="bold"),
            email_field,
            password_field,
            ft.ElevatedButton("Login", on_click=do_login),
            ft.TextButton("Don't have an account? Sign up", on_click=go_to_signup),
            login_status
        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        login_container = ft.Container(
            content=login_column,
            alignment=ft.alignment.center,
            expand=True
        )

        login_stack = ft.Stack([
            ft.Image(
                src="https://images.unsplash.com/photo-1584697964383-c3f9a9729f0e",
                fit=ft.ImageFit.COVER,
                width=page.width,
                height=page.height,
                opacity=0.4
            ),
            login_container
        ], expand=True)

        page.add(login_stack)
        page.update()

    def show_signup():
        page.controls.clear()

        name_field = ft.TextField(label="Name", width=300)
        email_field = ft.TextField(label="Email", width=300)
        password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
        signup_status = ft.Text(value="")

        def do_signup(e):
            res = requests.post(API_SIGNUP, json={"name": name_field.value, "email": email_field.value, "password": password_field.value})
            if res.status_code == 201:
                signup_status.value = "✅ Signup successful! Please login."
            else:
                signup_status.value = f"❌ {res.json().get('error', 'Signup failed')}"
            page.update()

        def go_to_login(e):
            show_login()

        signup_column = ft.Column([
            ft.Text("🆕 Create a Transcripto Account", size=24, weight="bold"),
            name_field,
            email_field,
            password_field,
            ft.ElevatedButton("Sign Up", on_click=do_signup),
            ft.TextButton("Already have an account? Login", on_click=go_to_login),
            signup_status
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, expand=True, width=400)

        signup_stack = ft.Stack([
            ft.Image(src="https://images.unsplash.com/photo-1584697964383-c3f9a9729f0e", fit=ft.ImageFit.COVER, width=page.width, height=page.height),
            signup_column
        ], expand=True)

        page.add(signup_stack)
        page.update()

    def show_main_ui():
        page.controls.clear()
        transcript_output = ft.Text(value="", selectable=True)
        summary_output = ft.Text(value="", selectable=True)
        qa_column = ft.Column(spacing=10)
        question_field = ft.TextField(label="Ask a question", expand=True)
        status_text = ft.Text(value=f"🎯 Selected: {selected_user_type['value']}", size=16, color=ft.colors.BLUE_600)

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

        user_types = {
            "Students and Researchers": "Students",
            "Businesses and Professionals": "Business",
            "Podcasters and Journalists": "Journalists",
            "General Users": "General"
        }

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
        user_type_buttons = user_type_row.controls[1:]

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
                    res = response.json()
                    answer = res.get("answer", "⚠️ No answer received.")
                    qa_column.controls.append(ft.Text(f"❓ Q: {q}", weight="bold"))
                    qa_column.controls.append(ft.Text(f"💡 A: {answer}"))
                    question_field.value = ""
                    status_text.value = "✅ Answer generated!"
                else:
                    status_text.value = f"❌ Server error: {response.status_code}"

            except Exception as ex:
                status_text.value = f"❌ Error: {str(ex)}"

            page.update()

        file_picker = ft.FilePicker(on_result=upload_file)
        page.overlay.append(file_picker)

        ask_button = ft.ElevatedButton("Ask", on_click=ask_question)

        page.add(
            ft.Text(f"🎙️ Welcome, {current_user['name']}", size=20),
            ft.ElevatedButton("Log out", icon=ft.icons.LOGOUT, on_click=lambda e: show_login()),
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
        page.update()

    # Start with login
    show_login()

ft.app(target=main)

