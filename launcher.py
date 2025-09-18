import os
import signal
import subprocess
from dotenv import load_dotenv

# Load env vars
load_dotenv()

processes = []

def start_process(command, cwd=None):
    """Helper to start subprocess and track it"""
    proc = subprocess.Popen(command, cwd=cwd, shell=True)
    processes.append(proc)
    return proc

def main():
    print("Starting all services...")

    # Start Python bot
    start_process(f'python "./AI-chan(discord)/index.py"')

    # Start Node server
    start_process(f'node "./vrm-chat-back/server.js"')

    # Start Ollama batch (still using .bat for now)
    start_process(f'"./Ollama Scripts/ollama_start.bat"')

    print("✅ All processes launched. Press CTRL+C to stop.")

    try:
        # Wait for children to finish (keeps launcher running)
        for proc in processes:
            proc.wait()
    except KeyboardInterrupt:
        shutdown()

def shutdown():
    print("\nShutting down all processes...")
    for proc in processes:
        if proc.poll() is None:  # still running
            proc.send_signal(signal.SIGTERM)
    print("All stopped.")
    exit(0)

if __name__ == "__main__":
    main()
