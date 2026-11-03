import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def apply_global_stylesheet(app):
    """Applies a 'Linux Hacker' green-on-black dark theme globally."""
    stylesheet = """
        QMainWindow, QWidget {
            background-color: #121212;
            color: #00ff00;
            font-family: 'Segoe UI', 'Ubuntu', 'Roboto', sans-serif;
            font-size: 13px;
        }
        QPushButton {
            background-color: #1e1e1e;
            color: #00ff00;
            border: 1px solid #005500;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #003300;
            border: 1px solid #00ff00;
        }
        QPushButton:pressed {
            background-color: #00ff00;
            color: #000000;
        }
        QPushButton:disabled {
            border: 1px solid #333333;
            color: #555555;
            background-color: #1a1a1a;
        }
        QComboBox {
            background-color: #1e1e1e;
            color: #00ff00;
            border: 1px solid #005500;
            border-radius: 4px;
            padding: 6px;
        }
        QComboBox:hover {
            border: 1px solid #00ff00;
        }
        QComboBox::drop-down {
            border-left: 1px solid #005500;
            width: 20px;
        }
        QComboBox QAbstractItemView {
            background-color: #1e1e1e;
            color: #00ff00;
            selection-background-color: #005500;
            selection-color: #00ff00;
            border: 1px solid #005500;
        }
    """
    app.setStyleSheet(stylesheet)

def main():
    app = QApplication(sys.argv)
    apply_global_stylesheet(app)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
