#!/usr/bin/env python3
import sys
import os
import json
import requests
import subprocess
import shutil

# --- BeTer Configuration ---
CONFIG_DIR = os.path.expanduser("~/.config/beter")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
OLLAMA_HOST = "http://localhost:11434"
REQUEST_TIMEOUT = 180

MODELS = {
    "standard": {
        "name": "llama3.2:3b",
        "ram_needed": "~4GB",
        "description": "Fast and reliable for most tasks."
    },
    "high_quality": {
        "name": "gemma3:12b",
        "ram_needed": "~8GB",
        "description": "Slower, more advanced commands."
    }
}

BETER_SYSTEM_PROMPT = """
You are 'BeTer', a helpful and expert Linux terminal assistant.
Your sole purpose is to translate a user's plain English question into the single, most appropriate shell command.

RULES:
1.  ONLY provide the shell command as your response.
2.  Do NOT include any explanations, apologies, code blocks (like ```bash), or introductory text.
3.  If a user asks a question not about a Linux command, respond with: # Error: I can only provide Linux commands.
4.  For potentially destructive commands (e.g., `rm`, `dd`, `mkfs`), add a comment line above the command starting with '# WARNING:'.
"""

# --- Helper Functions ---
def clean_response(text):
    if text.startswith("```"):
        return '\n'.join(text.split('\n')[1:-1]).strip()
    return text.strip()

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

# --- Ollama Management ---
class OllamaManager:
    @staticmethod
    def is_installed():
        return shutil.which("ollama") is not None

    @staticmethod
    def is_service_running():
        try:
            requests.get(f"{OLLAMA_HOST}/api/tags", timeout=3)
            return True
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def get_installed_models():
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
            # Ollama's list format has one JSON object per line
            models_data = [json.loads(line) for line in result.stdout.strip().split('\n')]
            return [model['name'] for model in models_data]
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def pull_model(model_name):
        print(f"Pulling model '{model_name}'. This may take some time...")
        try:
            process = subprocess.Popen(["ollama", "pull", model_name], stdout=sys.stdout, stderr=sys.stderr)
            process.wait()
            if process.returncode == 0:
                print(f"\n✅ Model '{model_name}' pulled successfully.")
                return True
            else:
                print(f"\n❌ Error pulling model. Please check your internet connection and try again.")
                return False
        except FileNotFoundError:
            # This should be caught by is_installed, but as a fallback
            print("❌ Error: 'ollama' command not found.")
            return False

# --- Core Application Logic ---
def first_time_setup():
    print("--- BeTer First-Time Setup ---")

    # 1. Check if Ollama is installed
    if not OllamaManager.is_installed():
        print("❌ Error: Ollama is not installed.")
        print("Please install it by running the following command in your terminal, then run BeTer again:")
        print("\n  curl -fsSL https://ollama.com/install.sh | sh\n")
        sys.exit(1)

    # 2. Check if Ollama service is running
    if not OllamaManager.is_service_running():
        print("❌ Error: Ollama is installed, but the service is not running.")
        print("Please start the Ollama service in a separate terminal with the command:")
        print("\n  ollama serve\n")
        print("Then, you can run BeTer in another terminal.")
        sys.exit(1)

    print("✅ Ollama is installed and running.")

    # 3. Choose and pull model
    print("\nPlease choose a model for BeTer based on your available RAM:")
    print(f"1. Standard ({MODELS['standard']['ram_needed']}): {MODELS['standard']['description']} (Model: {MODELS['standard']['name']})")
    print(f"2. High-Quality ({MODELS['high_quality']['ram_needed']}): {MODELS['high_quality']['description']} (Model: {MODELS['high_quality']['name']})")

    choice = ""
    while choice not in ["1", "2"]:
        choice = input("Enter your choice (1/2): ")

    chosen_tier = "standard" if choice == "1" else "high_quality"
    model_name = MODELS[chosen_tier]['name']

    installed_models = OllamaManager.get_installed_models()
    if model_name not in installed_models:
        if not OllamaManager.pull_model(model_name):
            sys.exit(1) # Exit if pull fails
    else:
        print(f"✅ Model '{model_name}' is already installed.")

    config = {"chosen_model": model_name}
    save_config(config)
    print("\n--- Setup Complete! You can now use BeTer. ---")
    return config

def query_beter(model_name, user_prompt):
    api_url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": model_name,
        "system": BETER_SYSTEM_PROMPT,
        "prompt": user_prompt,
        "stream": False
    }

    try:
        response = requests.post(api_url, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        raw_response = response.json().get("response", "").strip()
        return clean_response(raw_response)
    except Exception as e:
        return f"# Error: Failed to get response from Ollama: {e}"

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("BeTer by Peter - Your AI Terminal Assistant")
        print("Usage: beter \"<your question in plain English>\"")
        print("Example: beter \"find all files larger than 100MB\"")
        sys.exit(0)

    config = load_config()
    if not config:
        config = first_time_setup()
        # After setup, we don't proceed with the first query to keep the UX clean.
        # The user can immediately run their command again.
        print(f"\nPlease run your command again:\n  beter \"{' '.join(sys.argv[1:])}\"")
        sys.exit(0)

    # On subsequent runs, if Ollama service has stopped, guide the user.
    if not OllamaManager.is_service_running():
        print("❌ Error: Ollama service is not running. Please start it with 'ollama serve'.")
        sys.exit(1)

    user_question = ' '.join(sys.argv[1:])
    model_to_use = config.get("chosen_model", MODELS['standard']['name'])

    command = query_beter(model_to_use, user_question)
    print(command)

if __name__ == "__main__":
    main()
