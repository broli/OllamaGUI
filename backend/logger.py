from PySide6.QtCore import QObject, Signal

class AppLogger(QObject):
    # Signal emitted whenever a log message is generated.
    # The signature is: log_message(message: str, is_error: bool)
    log_emitted = Signal(str, bool)

    def __init__(self):
        super().__init__()

    def info(self, message: str):
        self.log_emitted.emit(f"[INFO] {message}", False)
        
    def error(self, message: str):
        self.log_emitted.emit(f"[ERROR] {message}", True)

    def raw(self, message: str, is_error: bool = False):
        self.log_emitted.emit(message, is_error)

# Global logger instance
logger = AppLogger()
