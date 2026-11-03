# OllamaGUI 🦙💻

A simple, personal desktop application built to manage local [Ollama](https://ollama.com) services, models, and status easily. 

This is a personal project I created to have a straightforward, native GUI to start/stop the Ollama service, check its status, download new models, and interact with them without needing to constantly use the command line. It's built with Python and PySide6 (Qt) to be lightweight, fast, and responsive.

---

## ✨ Features

- **Service Management**: Easily check the status of the local Ollama background service, and start or stop it directly from the app.
- **Model Management**: View your locally installed models, pull/download new ones, and manage your local Ollama library.
- **Quick Chat Interface**: A built-in, simple chat interface to test your local models and interact with them using a clean UI.
- **Native Desktop App**: Fast and lightweight GUI powered by Qt (PySide6) with a hacker-inspired dark theme.
- **Fully Local**: Fully offline, private, and secure—interacting directly with your local Ollama instance (`http://localhost:11434`).

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **GUI Framework**: [PySide6 (Qt for Python)](https://doc.qt.io/qtforpython-6/)
- **Backend API**: [Ollama Python Library](https://github.com/ollama/ollama-python)

---

## 🚀 Getting Started

### Prerequisites

Ensure you have **Ollama** installed on your local machine:
- Download & Install from: [ollama.com](https://ollama.com)

### Local Installation & Setup

1. **Clone this repository**:
   ```bash
   git clone <repo-url>
   cd OllamaGUI
   ```

2. **Set up the Python Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python main.py
   ```

---

## 📄 License

This project is open-source and licensed under the MIT License.
