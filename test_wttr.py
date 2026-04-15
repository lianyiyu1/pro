#!/usr/bin/env python3
# Test wttr.in access

import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from practice02.tools import curl

# Test with wttr.in
test_urls = [
    "https://wttr.in",
    "https://wttr.in/beijing",
    "https://wttr.in/chengdu"
]

for url in test_urls:
    print(f"\nTesting URL: {url}")
    print("=" * 40)
    
    result = curl(url, timeout=10)
    print(f"Success: {result.get('success', False)}")
    
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Status code: {result['status_code']}")
        print(f"Content length: {result['content_length']}")
        if result['content_length'] > 0:
            print(f"Content preview: {result['content'][:100]}...")

print("\nAll tests completed!")
