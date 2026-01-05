#!/usr/bin/env python3
"""
Entrypoint script that downloads assets and starts Streamlit.
"""
import sys
import subprocess

def main():
    # Download assets first
    print("Downloading assets...")
    try:
        from app.scripts.download_assets import main as download_main
        download_main()
    except Exception as e:
        print(f"Warning: Asset download failed: {e}")
        print("Continuing anyway...")
    
    # Start Streamlit (this replaces the Python process)
    print("Starting Streamlit...")
    sys.exit(subprocess.run([
        "streamlit", "run", 
        "app/main.py",
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ]).returncode)

if __name__ == "__main__":
    main()