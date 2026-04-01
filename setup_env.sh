#!/bin/bash

VENV_NAME="venv"

echo "🔍 Checking for Virtual Environment..."

if [ ! -d "$VENV_NAME" ]; then
    echo "🛠️ Creating Virtual Environment: $VENV_NAME..."
    python3 -m venv $VENV_NAME
else
    echo "✅ Virtual Environment already exists."
fi

echo "⚡ Activating Environment..."
source $VENV_NAME/bin/activate

echo "📦 Updating Pip and Installing Requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo -e "\n🎉 SETUP COMPLETE!"
echo "To start working, run: source venv/bin/activate"