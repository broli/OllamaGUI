# OllamaGUI 🦙💻

A premium, modern desktop interface built with **Python** and **PySide6 (Qt)** to interact with and manage your local **Ollama** models. 

Beautiful, responsive, and fast. Get the full power of local LLMs with a native, GPU-optimized desktop application.

---

## ✨ Features

- **🚀 Native Desktop App**: Fast, smooth, and lightweight GUI powered by Qt (PySide6).
- **🦙 Local First**: Fully offline, private, and secure interface interacting directly with your local Ollama instance (`http://localhost:11434`).
- **💬 Sleek Chat Interface**: Beautiful conversation layout with Markdown rendering, syntax highlighting, and smooth scrolling.
- **📦 Model Manager**: Easily download, delete, and inspect details of local Ollama models.
- **⚙️ Advanced Settings**: Configure temperature, system prompt, context window, and other generation parameters on the fly.
- **🎨 Modern Dark Mode**: Clean, premium aesthetics with tailored color palettes, glassmorphic touches, and elegant animations.

---

## 🛠️ Tech Stack

- **GUI Framework**: [PySide6 (Qt for Python)](https://doc.qt.io/qtforpython-6/)
- **Backend API**: [Ollama Python Library](https://github.com/ollama/ollama-python)
- **Styling**: Modern, custom QSS (Qt Style Sheets) for a gorgeous UI/UX
- **Language**: Python 3.10+

---

## 🚀 Getting Started

### Prerequisites

Ensure you have **Ollama** installed and running on your local machine:
- Download & Install from: [ollama.com](https://ollama.com)
- Ensure the server is running (usually at `http://localhost:11434`)

### Local Installation & Setup

1. **Clone this repository** (or use the created repository):
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

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
