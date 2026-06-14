from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QComboBox, QPlainTextEdit, QLabel
)
from PySide6.QtGui import QTextCursor
from backend.logger import logger

class SettingsTab(QWidget):
    def __init__(self, ollama_manager):
        super().__init__()
        self.ollama_manager = ollama_manager
        
        self.ollama_manager.models_updated.connect(self.update_model_dropdown)
        self.ollama_manager.service_status_changed.connect(self.update_ui_state)
        logger.log_emitted.connect(self.append_log)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Upper Panel: Controls
        controls_layout = QHBoxLayout()
        
        self.btn_start = QPushButton("Start Ollama Service")
        self.btn_start.clicked.connect(self.ollama_manager.start_service)
        
        self.btn_stop = QPushButton("Stop Ollama Service")
        self.btn_stop.clicked.connect(self.ollama_manager.stop_service)
        self.btn_stop.setEnabled(False) # Initially disabled

        self.btn_fetch = QPushButton("Fetch Models")
        self.btn_fetch.clicked.connect(self.ollama_manager.fetch_models)

        self.combo_models = QComboBox()
        self.combo_models.setMinimumWidth(250)
        self.combo_models.currentTextChanged.connect(self.ollama_manager.set_current_model)

        controls_layout.addWidget(self.btn_start)
        controls_layout.addWidget(self.btn_stop)
        controls_layout.addWidget(self.btn_fetch)
        
        model_label = QLabel("Model:")
        model_label.setStyleSheet("font-weight: bold;")
        controls_layout.addWidget(model_label)
        controls_layout.addWidget(self.combo_models)
        
        controls_layout.addStretch()

        main_layout.addLayout(controls_layout)

        # Lower Panel: Terminal Emulator
        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0c0c0c;
                color: #00ff00;
                font-family: 'Courier New', Courier, monospace;
                font-size: 14px;
                border: 2px solid #005500;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        self.terminal.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        
        main_layout.addWidget(self.terminal)

    def append_log(self, message: str, is_error: bool):
        # Save horizontal scroll position to prevent jumping to the right
        h_scrollbar = self.terminal.horizontalScrollBar()
        h_value = h_scrollbar.value()

        self.terminal.moveCursor(QTextCursor.MoveOperation.End)
        
        if is_error:
            self.terminal.appendHtml(f"<span style='color: #ff3333; font-family: monospace;'>{message}</span>")
        else:
            if message.startswith("[INFO]"):
                self.terminal.appendHtml(f"<span style='color: #00ccff; font-family: monospace;'>{message}</span>")
            else:
                self.terminal.appendPlainText(message)
            
        self.terminal.moveCursor(QTextCursor.MoveOperation.End)
        
        # Restore horizontal scroll position
        h_scrollbar.setValue(h_value)

    def update_model_dropdown(self, models):
        current_model = self.combo_models.currentText()
        self.combo_models.blockSignals(True)
        self.combo_models.clear()
        if models:
            self.combo_models.addItems(models)
            if current_model in models:
                self.combo_models.setCurrentText(current_model)
            self.ollama_manager.set_current_model(self.combo_models.currentText())
        else:
            self.combo_models.addItem("No models found")
            self.ollama_manager.set_current_model("")
        self.combo_models.blockSignals(False)

    def update_ui_state(self, is_running):
        self.btn_start.setEnabled(not is_running)
        self.btn_stop.setEnabled(is_running)

    def disable_controls(self):
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(False)
        self.btn_fetch.setEnabled(False)
