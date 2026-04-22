#!/usr/bin/env python3
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Importing main function...")
sys.stdout.flush()

try:
    from practice4.chat_with_summary import main
    print("Imported main function successfully")
    sys.stdout.flush()
    
    print("Calling main function...")
    sys.stdout.flush()
    main()
    
    print("Main function completed")
    sys.stdout.flush()
    
except Exception as e:
    print("Error: " + str(e))
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
