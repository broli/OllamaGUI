from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from backend.ollama_manager import OllamaManager
from backend.logger import logger
from ui.settings_tab import SettingsTab
from ui.chat_tab import ChatTab
from ui.models_tab import ModelsTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OllamaGUI - Local LLM Manager")
        self.resize(950, 700)
        
        # Backend initialization
        self.ollama_manager = OllamaManager()

        self.setup_ui()
        logger.info("Application initialized. Ready.")

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Tab Widget Configuration
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.West)
        
        # Apply style specifically to tab widget to match aesthetic
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #1a1a1a;
                color: #00ff00;
                border: 1px solid #005500;
                padding: 10px 20px;
                margin-bottom: 2px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #003300;
                border: 1px solid #00ff00;
            }
            QTabBar::tab:hover {
                background: #004400;
            }
            QTabWidget::pane {
                border: 1px solid #005500;
                background-color: #121212;
            }
        """)

        # Add tabs
        self.settings_tab = SettingsTab(self.ollama_manager)
        self.chat_tab = ChatTab(self.ollama_manager)
        self.models_tab = ModelsTab(self.ollama_manager)

        self.tabs.addTab(self.settings_tab, "Settings")
        self.tabs.addTab(self.chat_tab, "Chat")
        self.tabs.addTab(self.models_tab, "Models")

        main_layout.addWidget(self.tabs)

    def closeEvent(self, event):
        """Intercept the window close to ensure clean shutdown."""
        logger.info("Initiating safe shutdown sequence...")
        self.settings_tab.disable_controls()
        
        # Stop service synchronously before quitting
        self.ollama_manager.stop_service()
        event.accept()
