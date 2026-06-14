#!/bin/bash

# Configuration
APP_NAME="OllamaGUI"
APP_DIR="$HOME/.local/share/$APP_NAME"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "Deploying $APP_NAME..."

# 1. Create Application Directory
echo "Creating application directory at $APP_DIR..."
mkdir -p "$APP_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"

# 2. Copy application files
echo "Copying files..."
cp -r main.py backend ui requirements.txt ollama-vector-logo-seeklogo "$APP_DIR/"

# 3. Setup Virtual Environment
echo "Setting up virtual environment in $APP_DIR/.venv..."
cd "$APP_DIR"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# 4. Create launcher in ~/.local/bin
echo "Creating launcher in $BIN_DIR/ollamagui..."
cat > "$BIN_DIR/ollamagui" << EOF
#!/bin/bash
export APP_DIR="$APP_DIR"
exec "\$APP_DIR/.venv/bin/python" "\$APP_DIR/main.py" "\$@"
EOF

chmod +x "$BIN_DIR/ollamagui"

# 5. Create Desktop Entry
echo "Creating .desktop file..."
cat > "$DESKTOP_DIR/OllamaGUI.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=OllamaGUI
Comment=Custom Python desktop application to manage and interact with a local Ollama instance.
Exec=$BIN_DIR/ollamagui
Icon=$APP_DIR/ollama-vector-logo-seeklogo/ollama-seeklogo.png
Terminal=false
Categories=Utility;Development;
StartupNotify=true
EOF

chmod +x "$DESKTOP_DIR/OllamaGUI.desktop"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR"
fi

echo "Deployment complete!"
echo "You can now run 'ollamagui' from your terminal or launch $APP_NAME from your application menu."
