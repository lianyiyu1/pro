#!/usr/bin/env python3
# Test URL cleaning and encoding

import sys
import os
from urllib.parse import quote, urlparse, urlunparse

# Test the problematic URL
problematic_url = " `https://wttr.in/青城山?lang=zh-CN&t=q` "
print(f"Original URL: {problematic_url}")
print(f"Stripped: {problematic_url.strip()}")
print(f"Strip backticks: {problematic_url.strip().strip('`')}")

# Test the cleaning process
url = problematic_url.strip().strip('`')
print(f"\nCleaned URL: {url}")

# Parse and encode
parsed = urlparse(url)
print(f"\nParsed components:")
print(f"Scheme: {parsed.scheme}")
print(f"Netloc: {parsed.netloc}")
print(f"Path: {parsed.path}")
print(f"Query: {parsed.query}")

# Encode path
encoded_path = quote(parsed.path, safe='/:')
print(f"\nEncoded path: {encoded_path}")

# Reconstruct URL
encoded_url = urlunparse((
    parsed.scheme,
    parsed.netloc,
    encoded_path,
    parsed.params,
    parsed.query,
    parsed.fragment
))
print(f"\nFinal encoded URL: {encoded_url}")

# Test with the actual curl function
print("\n" + "="*50)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from practice02.tools import curl

result = curl(problematic_url, timeout=5)
print(f"Success: {result.get('success', False)}")
if 'error' in result:
    print(f"Error: {result['error']}")
else:
    print(f"Status code: {result['status_code']}")
    print(f"Encoded URL: {result['encoded_url']}")

print("\nTest completed!")
