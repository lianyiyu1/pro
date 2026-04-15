#!/usr/bin/env python3
# Test script for weather fetching

import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from practice02.tools import curl

# Test with wttr.in for Qingcheng Mountain
test_url = "https://wttr.in/青城山"
print(f"Testing weather for Qingcheng Mountain: {test_url}")

result = curl(test_url, timeout=10)
print("\nTest result:")
print(f"Success: {result.get('success', False)}")
if 'error' in result:
    print(f"Error: {result['error']}")
else:
    print(f"Status code: {result['status_code']}")
    print(f"Encoded URL: {result['encoded_url']}")
    print(f"Content length: {result['content_length']}")
    print(f"\nWeather information:")
    print(result['content'])

print("\nTest completed!")
