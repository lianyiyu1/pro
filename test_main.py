#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing main function...")

try:
    from practice4.chat_with_summary import main
    print("Imported main function successfully")
    print("Calling main function...")
    # Call main function with a timeout to prevent it from hanging
    import threading
    import time
    
    def run_main():
        try:
            main()
        except Exception as e:
            print(f"Error in main function: {e}")
            import traceback
            traceback.print_exc()
    
    thread = threading.Thread(target=run_main)
    thread.daemon = True
    thread.start()
    
    # Wait for 5 seconds
    time.sleep(5)
    
    if thread.is_alive():
        print("Main function is still running (likely waiting for user input)")
    else:
        print("Main function completed")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("Test completed")
