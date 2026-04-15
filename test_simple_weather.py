#!/usr/bin/env python3
# Simple test for wttr.in

import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from practice02.tools import curl

# Test with simple URL
test_url = "https://wttr.in/chengdu?0"
print(f"Testing URL: {test_url}")

result = curl(test_url, timeout=5)
print(f"Success: {result.get('success', False)}")
if 'error' in result:
    print(f"Error: {result['error']}")
else:
    print(f"Status code: {result['status_code']}")
    print(f"Content: {result['content']}")

print("Test completed!")
