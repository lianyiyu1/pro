#!/usr/bin/env python3
# Test different wttr.in URL formats

import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from practice02.tools import curl

# Test different URL formats
test_urls = [
    "https://wttr.in/chengdu",
    "https://wttr.in/chengdu?m",
    "https://wttr.in/chengdu?0",
    "https://wttr.in/chengdu?format=3",
    "https://wttr.in/qingchengshan",
    "https://wttr.in/qingchengshan?0",
    "https://www.baidu.com/s?wd=青城山天气"
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
        print(f"Content length: {result['content_length']}")
        if result['content_length'] > 0:
            # For text formats, show more content
            if 'format' in url or '0' in url:
                print(f"Content: {result['content'][:500]}")
            else:
                print(f"Content preview: {result['content'][:100]}...")

print("\nAll tests completed!")
