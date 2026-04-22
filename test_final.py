#!/usr/bin/env python3
import sys

print("Starting script...")
sys.stdout.flush()

try:
    import os
    import time
    print("Imported modules")
    sys.stdout.flush()
    
    # Get current date
    current_date = time.strftime('%Y-%m-%d')
    print("Current date: " + current_date)
    sys.stdout.flush()
    
    # Test f-string
    test_string = f"Test f-string: {current_date}"
    print(test_string)
    sys.stdout.flush()
    
    print("Script completed successfully!")
    sys.stdout.flush()
    
except Exception as e:
    print("Error: " + str(e))
    sys.stdout.flush()
