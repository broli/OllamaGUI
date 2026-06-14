from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTextBrowser, QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor

class ChatTab(QWidget):
    def __init__(self, ollama_manager):
        super().__init__()
        self.ollama_manager = ollama_manager
        
        self.ollama_manager.chat_chunk_received.connect(self.on_chat_chunk)
        self.ollama_manager.chat_finished.connect(self.on_chat_finished)
        self.ollama_manager.chat_error.connect(self.on_chat_error)

        self.messages = [] # Format: [{'role': 'user', 'content': '...'}, ...]
        self.current_response = ""

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        self.chat_history = QTextBrowser()
        self.chat_history.setOpenExternalLinks(True)
        self.chat_history.setStyleSheet("""
            QTextBrowser {
                background-color: #0c0c0c;
                color: #e0e0e0;
                font-family: 'Segoe UI', 'Ubuntu', sans-serif;
                font-size: 14px;
                border: 1px solid #333;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        main_layout.addWidget(self.chat_history, stretch=1)

        input_layout = QHBoxLayout()
        
        self.text_input = QTextEdit()
        self.text_input.setMaximumHeight(80)
        self.text_input.setPlaceholderText("Type your message to the LLM here...")
        self.text_input.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #00ff00;
                border: 1px solid #005500;
                border-radius: 4px;
            }
        """)
        input_layout.addWidget(self.text_input)

        self.btn_send = QPushButton("Send")
        self.btn_send.setMinimumHeight(80)
        self.btn_send.clicked.connect(self.send_message)
        input_layout.addWidget(self.btn_send)

        main_layout.addLayout(input_layout)

    def render_chat(self):
        html = ""
        for msg in self.messages:
            if msg['role'] == 'user':
                content = msg['content'].replace('\n', '<br>')
                html += f"<div style='text-align: right; margin-bottom: 10px;'><span style='background-color: #004400; color: #00ff00; padding: 5px 10px; border-radius: 5px; font-weight: bold;'>You</span><br><div style='text-align: right; color: #aaffaa; margin-top: 5px;'>{content}</div></div><hr style='border: 1px solid #222;'/>"
            elif msg['role'] == 'assistant':
                content = msg['content'].replace('\n', '<br>')
                html += f"<div style='text-align: left; margin-bottom: 10px;'><span style='color: #00ccff; font-weight: bold;'>Ollama</span><br><div style='color: #e0e0e0; margin-top: 5px;'>{content}</div></div><hr style='border: 1px solid #222;'/>"
        
        if self.current_response:
            content = self.current_response.replace('\n', '<br>')
            html += f"<div style='text-align: left; margin-bottom: 10px;'><span style='color: #00ccff; font-weight: bold;'>Ollama</span><br><div style='color: #e0e0e0; margin-top: 5px;'>{content}</div></div>"
            
        self.chat_history.setHtml(html)
        self.chat_history.moveCursor(QTextCursor.MoveOperation.End)

    def send_message(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            return
            
        model = self.ollama_manager.get_current_model()
        if not model:
            self.chat_history.append("<div style='color: red;'>Please select a model in the settings tab first.</div>")
            return
            
        self.messages.append({'role': 'user', 'content': text})
        self.text_input.clear()
        self.btn_send.setEnabled(False)
        self.text_input.setEnabled(False)
        
        self.current_response = ""
        self.render_chat()
        
        self.ollama_manager.send_chat(model, self.messages.copy())

    def on_chat_chunk(self, chunk):
        self.current_response += chunk
        self.render_chat()

    def on_chat_finished(self):
        self.messages.append({'role': 'assistant', 'content': self.current_response})
        self.current_response = ""
        self.render_chat()
        
        self.btn_send.setEnabled(True)
        self.text_input.setEnabled(True)
        self.text_input.setFocus()

    def on_chat_error(self, error):
        self.chat_history.append(f"<div style='color: red;'>Error: {error}</div>")
        self.btn_send.setEnabled(True)
        self.text_input.setEnabled(True)
