#!/usr/bin/env python3
# Test script for curl tool

import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from practice02.tools import curl

# Test with simple URL
test_url = "https://www.baidu.com"
print(f"Testing URL: {test_url}")

result = curl(test_url, timeout=10)
print("\nTest result:")
print(f"Success: {result.get('success', False)}")
if 'error' in result:
    print(f"Error: {result['error']}")
else:
    print(f"Status code: {result['status_code']}")
    print(f"Encoded URL: {result['encoded_url']}")
    print(f"Content length: {result['content_length']}")
    print(f"Content preview: {result['content'][:200]}...")

print("\nTest completed!")
