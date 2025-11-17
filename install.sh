#!/bin/bash

# Get the absolute path of the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SOURCE_FILE="$SCRIPT_DIR/beter.py"
INSTALL_PATH="/usr/local/bin/beter"

echo "BeTer by Peter Installer"

# 1. Check if beter.py exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: beter.py not found in the same directory as the installer."
    exit 1
fi

# 2. Make the python script executable
echo "Making beter.py executable..."
chmod +x "$SOURCE_FILE"

# 3. Create a symbolic link in /usr/local/bin
echo "Creating symbolic link at $INSTALL_PATH..."
echo "This requires administrator privileges."
if sudo ln -sf "$SOURCE_FILE" "$INSTALL_PATH"; then
    echo "-----------------------------------------------------"
    echo "✅ Success! 'beter' is now installed."
    echo "You can now run it from anywhere in your terminal."
    echo "Example: beter \"how to check disk space\""
    echo "-----------------------------------------------------"
else
    echo "❌ Error: Failed to create symbolic link. Please check permissions."
    exit 1
fi
