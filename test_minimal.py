#!/usr/bin/env python3
#-*- coding: utf-8 -*-
print("Hello, World!")
print("Testing minimal script...")

# Test 1: Basic print
print("Test 1: Basic print works")

# Test 2: Import modules
print("Test 2: Importing modules...")
try:
    import os
    import json
    import time
    print("Imported modules successfully")
except Exception as e:
    print(f"Error importing modules: {e}")

# Test 3: Read .env file
print("Test 3: Reading .env file...")
try:
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        print(f".env file exists at {env_path}")
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f".env file content: {content[:100]}...")
    else:
        print(".env file not found")
except Exception as e:
    print(f"Error reading .env file: {e}")

# Test 4: Time function
print("Test 4: Testing time function...")
try:
    current_date = time.strftime('%Y-%m-%d')
    print(f"Current date: {current_date}")
except Exception as e:
    print(f"Error getting current date: {e}")

# Test 5: f-string
print("Test 5: Testing f-string...")
try:
    test_var = "test"
    test_string = f"This is a {test_var}"
    print(f"f-string works: {test_string}")
except Exception as e:
    print(f"Error with f-string: {e}")

print("\nAll tests completed!")
