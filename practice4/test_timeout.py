#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
import os
import time

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_with_summary import LLMClient

# Test the LLMClient.chat() method with timeout
def test_timeout():
    print("Testing LLMClient.chat() with timeout...")
    
    try:
        # Initialize LLM client
        client = LLMClient()
        print(f"Connected to: {client.model}")
        print(f"Base URL: {client.base_url}")
        
        # Create a simple chat history
        chat_history = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Hello, how are you?"
            }
        ]
        
        # Test the chat method with timeout
        start_time = time.time()
        print("\nSending chat request...")
        result = client.chat(chat_history)
        end_time = time.time()
        
        print(f"Request completed in {end_time - start_time:.2f} seconds")
        print(f"Response content: {result['content']}")
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_timeout()
