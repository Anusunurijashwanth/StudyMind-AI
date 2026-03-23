import subprocess
import sys
import time
import requests

# Check if Ollama is running
def check_ollama():
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=3)
        if resp.status_code == 200:
            print("[✔] Ollama AI server is running.")
            return True
    except:
        print("[⚠] Ollama AI server not reachable at localhost:11434.")
    return False


def start_ollama():
    print("[ℹ] Please start Ollama manually in another terminal with:")
    print("     ollama serve")
    input("Press Enter after starting Ollama...")


def start_fastapi():
    print("[ℹ] Starting FastAPI server...")

    subprocess.Popen([
        sys.executable,
        "-m",
        "uvicorn",
        "app:app",
        "--reload",
        "--host",
        "127.0.0.1",
        "--port",
        "8000"
    ])

    time.sleep(2)

    print("[✔] FastAPI started")
    print("Swagger UI → http://127.0.0.1:8000/docs")


if __name__ == "__main__":

    if not check_ollama():
        start_ollama()

    start_fastapi()