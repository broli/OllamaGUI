from PySide6.QtCore import QObject, QProcess, Signal, QThread
import ollama
from backend.logger import logger
import re

class ChatWorker(QThread):
    chunk_received = Signal(str)
    chat_finished = Signal()
    error_occurred = Signal(str)

    def __init__(self, model: str, messages: list):
        super().__init__()
        self.model = model
        self.messages = messages

    def run(self):
        try:
            stream = ollama.chat(
                model=self.model,
                messages=self.messages,
                stream=True,
            )
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    self.chunk_received.emit(chunk['message']['content'])
            self.chat_finished.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

class PullWorker(QThread):
    progress_updated = Signal(int)
    status_updated = Signal(str)
    pull_finished = Signal()
    error_occurred = Signal(str)

    def __init__(self, model: str):
        super().__init__()
        self.model = model

    def run(self):
        try:
            stream = ollama.pull(self.model, stream=True)
            for chunk in stream:
                status = chunk.get('status', 'Downloading...')
                self.status_updated.emit(status)
                
                if 'total' in chunk and 'completed' in chunk:
                    total = chunk['total']
                    completed = chunk['completed']
                    if total > 0:
                        percent = int((completed / total) * 100)
                        self.progress_updated.emit(percent)
            
            self.pull_finished.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

class ModelFetcher(QThread):
    models_fetched = Signal(list)
    error_occurred = Signal(str)

    def run(self):
        try:
            # ollama.list() returns a dict with 'models' key
            response = ollama.list()
            # If ollama api returns objects directly
            models = []
            if hasattr(response, 'models'):
                models = [model.model for model in response.models]
            elif isinstance(response, dict) and 'models' in response:
                models = [model.get('name', 'unknown') for model in response['models']]
            else:
                models = []
                
            self.models_fetched.emit(models)
        except Exception as e:
            self.error_occurred.emit(str(e))

class OllamaManager(QObject):
    models_updated = Signal(list)
    service_status_changed = Signal(bool) # True if running, False if stopped
    
    # Chat signals
    chat_chunk_received = Signal(str)
    chat_finished = Signal()
    chat_error = Signal(str)
    
    # Pull signals
    pull_progress_updated = Signal(int)
    pull_status_updated = Signal(str)
    pull_finished = Signal()
    pull_error = Signal(str)

    def __init__(self):
        super().__init__()
        self.process = QProcess()
        self.process.setProgram("ollama")
        self.process.setArguments(["serve"])
        
        # Connect process signals
        self.process.readyReadStandardOutput.connect(self._handle_stdout)
        self.process.readyReadStandardError.connect(self._handle_stderr)
        self.process.stateChanged.connect(self._handle_state_change)
        self.process.errorOccurred.connect(self._handle_process_error)
        
        self._model_fetcher = None
        self._chat_worker = None
        self._pull_worker = None
        self.current_model = ""

    def set_current_model(self, model: str):
        self.current_model = model

    def get_current_model(self) -> str:
        return self.current_model

    def send_chat(self, model: str, messages: list):
        self._chat_worker = ChatWorker(model, messages)
        self._chat_worker.chunk_received.connect(self.chat_chunk_received.emit)
        self._chat_worker.chat_finished.connect(self.chat_finished.emit)
        self._chat_worker.error_occurred.connect(self.chat_error.emit)
        self._chat_worker.start()

    def pull_model(self, model: str):
        if self._pull_worker and self._pull_worker.isRunning():
            logger.error("A model is already being pulled.")
            return
            
        logger.info(f"Starting pull for model: {model}")
        self._pull_worker = PullWorker(model)
        self._pull_worker.progress_updated.connect(self.pull_progress_updated.emit)
        self._pull_worker.status_updated.connect(self.pull_status_updated.emit)
        self._pull_worker.pull_finished.connect(self.pull_finished.emit)
        self._pull_worker.error_occurred.connect(self.pull_error.emit)
        self._pull_worker.start()

    def start_service(self):
        if self.process.state() == QProcess.ProcessState.NotRunning:
            logger.info("Starting Ollama service (ollama serve)...")
            self.process.start()
        else:
            logger.info("Ollama service is already running.")

    def stop_service(self):
        if self.process.state() != QProcess.ProcessState.NotRunning:
            logger.info("Stopping Ollama service...")
            self.process.terminate()
            if not self.process.waitForFinished(3000): # Wait 3 seconds
                logger.error("Service did not terminate gracefully, forcing kill...")
                self.process.kill()
                self.process.waitForFinished(2000)
        else:
            logger.info("Ollama service is not running.")

    def fetch_models(self):
        logger.info("Fetching installed models...")
        self._model_fetcher = ModelFetcher()
        self._model_fetcher.models_fetched.connect(self._on_models_fetched)
        self._model_fetcher.error_occurred.connect(self._on_fetch_error)
        self._model_fetcher.start()

    def _on_models_fetched(self, models):
        logger.info(f"Successfully fetched {len(models)} models.")
        self.models_updated.emit(models)

    def _on_fetch_error(self, error_msg):
        logger.error(f"Failed to fetch models: {error_msg}")
        logger.error("Make sure the Ollama service is running!")

    def _clean_ansi(self, text: str) -> str:
        # Remove ANSI escape sequences (colors, control characters) which Ollama emits
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def _handle_stdout(self):
        output = self.process.readAllStandardOutput().data().decode('utf-8').strip()
        if output:
            for line in output.split('\n'):
                line = self._clean_ansi(line)
                if line.strip():
                    logger.raw(line, is_error=False)

    def _handle_stderr(self):
        output = self.process.readAllStandardError().data().decode('utf-8').strip()
        if output:
            for line in output.split('\n'):
                line = self._clean_ansi(line)
                if line.strip():
                    # Ollama typically logs normal behavior to stderr
                    logger.raw(line, is_error=False) 

    def _handle_state_change(self, state):
        if state == QProcess.ProcessState.Running:
            logger.info("Ollama service is now RUNNING.")
            self.service_status_changed.emit(True)
        elif state == QProcess.ProcessState.NotRunning:
            logger.info("Ollama service is now STOPPED.")
            self.service_status_changed.emit(False)

    def _handle_process_error(self, error):
        logger.error(f"Ollama process error: {self.process.errorString()}")
