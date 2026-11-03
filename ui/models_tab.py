from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QScrollArea, QFrame,
    QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from backend.logger import logger

CATALOG = [
    {"id": "llama3", "name": "Llama 3 (8B)", "developer": "Meta", "url": "https://ollama.com/library/llama3"},
    {"id": "phi3", "name": "Phi-3 Mini", "developer": "Microsoft", "url": "https://ollama.com/library/phi3"},
    {"id": "mistral", "name": "Mistral (7B)", "developer": "Mistral AI", "url": "https://ollama.com/library/mistral"},
    {"id": "gemma", "name": "Gemma (7B)", "developer": "Google", "url": "https://ollama.com/library/gemma"},
    {"id": "qwen2", "name": "Qwen2 (7B)", "developer": "Alibaba Cloud", "url": "https://ollama.com/library/qwen2"},
    {"id": "llava", "name": "LLaVA (Vision)", "developer": "Haotian Liu et al.", "url": "https://ollama.com/library/llava"},
    {"id": "mixtral", "name": "Mixtral 8x7B", "developer": "Mistral AI", "url": "https://ollama.com/library/mixtral"},
    {"id": "codellama", "name": "Code Llama (7B)", "developer": "Meta", "url": "https://ollama.com/library/codellama"},
]

class ModelCard(QFrame):
    def __init__(self, model_info, install_callback):
        super().__init__()
        self.model_info = model_info
        self.install_callback = install_callback
        
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            ModelCard {
                background-color: #1a1a1a;
                border: 1px solid #333;
                border-radius: 6px;
                margin-bottom: 5px;
            }
            ModelCard:hover {
                border: 1px solid #005500;
            }
        """)

        layout = QHBoxLayout(self)

        info_layout = QVBoxLayout()
        name_label = QLabel(self.model_info["name"])
        name_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #00ff00; border: none;")
        
        dev_label = QLabel(f"Developer: {self.model_info['developer']} | ID: {self.model_info['id']}")
        dev_label.setStyleSheet("color: #aaaaaa; font-size: 12px; border: none;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(dev_label)

        btn_layout = QVBoxLayout()
        self.btn_install = QPushButton("Install / Update")
        self.btn_install.clicked.connect(lambda: self.install_callback(self.model_info["id"]))
        
        self.btn_link = QPushButton("Open Homepage")
        self.btn_link.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #005500;
                color: #00ccff;
            }
            QPushButton:hover {
                background-color: #002233;
            }
        """)
        self.btn_link.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(self.model_info["url"])))

        btn_layout.addWidget(self.btn_install)
        btn_layout.addWidget(self.btn_link)

        layout.addLayout(info_layout, stretch=1)
        layout.addLayout(btn_layout)

class ModelsTab(QWidget):
    def __init__(self, ollama_manager):
        super().__init__()
        self.ollama_manager = ollama_manager
        
        self.ollama_manager.pull_progress_updated.connect(self.on_progress)
        self.ollama_manager.pull_status_updated.connect(self.on_status)
        self.ollama_manager.pull_finished.connect(self.on_finished)
        self.ollama_manager.pull_error.connect(self.on_error)
        
        self.current_pulling = ""
        self.cards = []
        
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Header
        header = QLabel("Popular Models Catalog")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #00ff00; margin-bottom: 10px;")
        main_layout.addWidget(header)

        # Scroll Area for Cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none; background-color: #121212;")
        
        scroll_widget = QWidget()
        self.cards_layout = QVBoxLayout(scroll_widget)
        self.cards_layout.setSpacing(10)
        
        for model in CATALOG:
            card = ModelCard(model, self.start_pull)
            self.cards.append(card)
            self.cards_layout.addWidget(card)
            
        self.cards_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        
        main_layout.addWidget(scroll_area, stretch=1)

        # Status and Progress Bar (Bottom)
        status_layout = QVBoxLayout()
        self.lbl_status = QLabel("Idle.")
        self.lbl_status.setStyleSheet("color: #aaaaaa;")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #005500;
                border-radius: 4px;
                text-align: center;
                background-color: #1a1a1a;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
                width: 10px;
            }
        """)
        
        status_layout.addWidget(self.lbl_status)
        status_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(status_layout)

    def set_buttons_enabled(self, enabled: bool):
        for card in self.cards:
            card.btn_install.setEnabled(enabled)

    def start_pull(self, model_id: str):
        self.current_pulling = model_id
        self.set_buttons_enabled(False)
        self.lbl_status.setText(f"Starting pull for {model_id}...")
        self.progress_bar.setValue(0)
        logger.info(f"Initiated pull for {model_id}")
        self.ollama_manager.pull_model(model_id)

    def on_progress(self, percent: int):
        self.progress_bar.setValue(percent)

    def on_status(self, status: str):
        self.lbl_status.setText(f"Pulling {self.current_pulling}: {status}")

    def on_finished(self):
        self.lbl_status.setText(f"Successfully pulled {self.current_pulling}!")
        self.progress_bar.setValue(100)
        logger.info(f"Finished pulling {self.current_pulling}")
        self.set_buttons_enabled(True)
        self.current_pulling = ""

    def on_error(self, error: str):
        self.lbl_status.setText(f"Error pulling model.")
        self.progress_bar.setValue(0)
        logger.error(f"Pull error: {error}")
        self.set_buttons_enabled(True)
        self.current_pulling = ""
