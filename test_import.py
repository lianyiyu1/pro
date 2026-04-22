#!/usr/bin/env python3
#-*- coding: utf-8 -*-
print("Hello, World!")
print("Testing Python imports...")

try:
    import os
    import json
    import time
    import sys
    from urllib.parse import urlparse
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
    print("Imported standard libraries successfully")
    
    # Add the project root directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from practice02.tools import list_files, rename_file, delete_file, create_file, read_file, curl
    print("Imported tools successfully")
    
    from practice4.chat_with_summary import load_env, LLMClient
    print("Imported chat_with_summary modules successfully")
    
    print("All imports successful!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("Test completed")
