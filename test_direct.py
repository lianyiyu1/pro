#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import os
import sys

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing direct execution...")

# Run the script directly
import subprocess

result = subprocess.run(
    [sys.executable, "practice4/chat_with_summary.py"],
    capture_output=True,
    text=True,
    encoding='utf-8'
)

print("Return code:", result.returncode)
print("\nSTDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)

print("\nTest completed")
