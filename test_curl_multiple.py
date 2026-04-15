#!/usr/bin/env python3
# Test script for curl tool with different URLs

import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from practice02.tools import curl

# Test URLs
test_urls = [
    "https://www.baidu.com",
    "https://wttr.in/beijing",  # Use English location name
    "https://api.weatherapi.com/v1/current.json?key=de6e5f274c964d038a3b01026041302&q=Beijing&lang=zh",
    "https://www.timeanddate.com/weather/china/beijing"
]

for url in test_urls:
    print(f"\nTesting URL: {url}")
    print("=" * 50)
    
    result = curl(url, timeout=10)
    print(f"Success: {result.get('success', False)}")
    
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Status code: {result['status_code']}")
        print(f"Encoded URL: {result['encoded_url']}")
        print(f"Content length: {result['content_length']}")
        print(f"Content preview: {result['content'][:100]}...")

print("\nAll tests completed!")
