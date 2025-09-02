#!/usr/bin/env python3
import subprocess
import sys
import os

if __name__ == "__main__":
    frontend_path = os.path.join(os.path.dirname(__file__), 'frontend')
    app_path = os.path.join(frontend_path, 'app.py')
    
    subprocess.run([
        sys.executable, 
        "-m", "streamlit", "run", app_path,
        "--server.port", "8501",
        "--server.headless", "true"
    ])