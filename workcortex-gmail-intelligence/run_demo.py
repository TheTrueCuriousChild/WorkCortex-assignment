#!/usr/bin/env python
"""
run_demo.py - Run the demo without needing Gmail credentials
Place in project root and run: python run_demo.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.main_demo import main

if __name__ == "__main__":
    sys.exit(main())
