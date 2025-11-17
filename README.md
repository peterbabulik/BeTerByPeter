# BeTer by Peter (Better Terminal)

### Your Private, AI-Powered Terminal Assistant 🧠💻

Ever forget the exact syntax for `tar` or `find`? Tired of switching to a browser to look up a simple command? **BeTer** is an AI-assisted terminal tool that translates your plain English questions into the shell commands you need, right where you need them.

It runs entirely on your local machine using [Ollama](https://ollama.com/), ensuring your queries are **100% private**. No data ever leaves your computer.

### Demo

**First-time setup and first query:**

**Example Usage:**
```bash
$ beter "find all markdown files modified in the last 2 days"
find . -name "*.md" -mtime -2

$ beter "how much disk space is free on my system in a human readable format"
df -h

$ beter "delete a directory named 'old-project' and everything in it"
# WARNING: This command can cause irreversible data loss.
rm -rf old-project/
```

## ✨ Key Features

*   **Natural Language Commands**: Ask for what you want in plain English.
*   **100% Local & Private**: Powered by Ollama, BeTer runs a local AI model on your machine. No internet connection is needed after setup, and your commands are never sent to a third-party service.
*   **Intelligent First-Time Setup**: The first time you run `beter`, it guides you through checking for Ollama and downloading the AI model of your choice.
*   **Model Selection**: Choose between a "Standard" model for speed and reliability on most machines, or a "High-Quality" model for more advanced commands on machines with more RAM.
*   **Safety First**: BeTer is designed to add a warning for potentially destructive commands (like `rm`, `dd`, `mkfs`) before presenting them.

## ⚙️ Installation

Installation is handled by a simple script.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/peterbabulik/BeTerByPeter.git
    ```

2.  **Navigate into the Directory**
    ```bash
    cd BeTerByPeter
    ```

3.  **if you want beter command, in bash (example: better "your qeustion here" , Run the Installer**
    ```bash
    chmod +x install.sh
    ./install.sh
    ```
    The installer will make the `beter.py` script executable and create a symbolic link in `/usr/local/bin`, so you can call `beter` from anywhere. It will ask for your password to do this.
    *restart terminal, or start new one*
 
## or you can run: python3 beter.py "find files larger than 100MB"
    ```bash
    python3 beter.py "find files larger than 100MB"
    ```

## 🚀 First Run & Usage

The first time you run `beter`, it will trigger the setup assistant:

1.  It will check if Ollama is installed and running. If not, it will provide instructions.
2.  You will be prompted to choose an AI model to download based on your system's RAM.
3.  The chosen model will be pulled from Ollama.

After the one-time setup is complete, you can use BeTer by simply typing `beter` followed by your question in quotes:

```bash
# Simple commands
beter "what is my current directory?"
beter "who is the current user?"

# More complex commands
beter "create a compressed tar archive of the 'my_project' directory"
beter "search for every line containing the word 'error' in the system log"
```

### Configuration

Your chosen model is saved in `~/.config/beter/config.json`. If you want to change the model or re-run the setup, simply delete this file and run `beter` again.

```bash
rm ~/.config/beter/config.json
```
