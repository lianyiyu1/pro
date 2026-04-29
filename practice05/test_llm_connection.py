#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import json
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Test LLM connection
def test_llm_connection():
    print("Testing LLM connection...")
    
    try:
        # Prepare request
        url = "http://127.0.0.1:1234/v1/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '
        }
        
        data = {
            'model': 'qwen/qwen3.5-9b',
            'messages': [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Hello, how are you?"
                }
            ],
            'temperature': 0.7,
            'max_tokens': 100,
            'stream': False
        }
        
        # Send request
        print("Sending request to LLM...")
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        print(f"Data: {json.dumps(data, ensure_ascii=False)}")
        
        req = Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        
        start_time = time.time()
        print(f"Request sent at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        with urlopen(req, timeout=60) as response:
            end_time = time.time()
            print(f"Response received at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Response time: {end_time - start_time:.2f} seconds")
            
            response_content = response.read().decode('utf-8', errors='replace')
            print(f"Response content length: {len(response_content)}")
            
            try:
                response_data = json.loads(response_content)
                print("Response JSON parsed successfully")
                print(json.dumps(response_data, indent=2, ensure_ascii=False))
                
                # Extract content
                if 'choices' in response_data and response_data['choices']:
                    content = response_data['choices'][0]['message'].get('content', '')
                    print("\nLLM response:")
                    print(content)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                print(f"Response content: {response_content}")
            
        print("\n✓ LLM connection test passed!")
        
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        try:
            error_content = e.read().decode('utf-8')
            print(f"Error content: {error_content}")
        except:
            pass
        import traceback
        traceback.print_exc()
    except URLError as e:
        print(f"URL Error: {e.reason}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting LLM connection test...")
    test_llm_connection()
    print("LLM connection test completed.")
