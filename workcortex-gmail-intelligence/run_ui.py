#!/usr/bin/env python
"""
run_ui.py - Run the Streamlit web UI
Place in project root and run: python run_ui.py
"""

import subprocess
import sys

if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "streamlit", "run", "ui/app.py"])
