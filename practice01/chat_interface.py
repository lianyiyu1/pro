#!/usr/bin/env python3
 #-*- coding: utf-8 -*-
import os
import json
import time
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def load_env():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    
    if not os.path.exists(env_path):
        raise FileNotFoundError(f".env file not found at {env_path}")
    
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars


class LLMClient:
    """OpenAI Compatible LLM Client with streaming support"""
    
    def __init__(self):
        self.env = load_env()
        self.base_url = self.env.get('LLM_BASE_URL', 'http://127.0.0.1:1234')
        self.model = self.env.get('LLM_MODEL', 'qwen/qwen3.5-9b')
        self.api_key = self.env.get('LLM_API_KEY', '123456')
        self.temperature = float(self.env.get('LLM_TEMPERATURE', '1'))
        self.max_tokens = int(self.env.get('LLM_MAX_TOKENS', '1000'))
        
        # Ensure base_url ends with /v1 if not already present
        if not self.base_url.endswith('/v1'):
            self.base_url = self.base_url.rstrip('/') + '/v1'
        
        if not all([self.base_url, self.model, self.api_key]):
            raise ValueError("Missing required LLM configuration in .env file")
    
    def chat_stream(self, messages):
        """Send chat completion request to LLM with streaming"""
        start_time = time.time()
        
        # Prepare request
        url = f"{self.base_url}/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        data = {
            'model': self.model,
            'messages': messages,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'stream': True  # Enable streaming
        }
        
        # Send request
        req = Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        
        try:
            with urlopen(req) as response:
                buffer = b''
                full_content = ""
                usage = {}
                
                # Read response in chunks for streaming
                while True:
                    chunk = response.read(1024)
                    if not chunk:
                        break
                    
                    buffer += chunk
                    
                    # Process complete lines only
                    while b'\n' in buffer:
                        line, buffer = buffer.split(b'\n', 1)
                        line = line.strip()
                        if not line:
                            continue
                        
                        # Remove 'data: ' prefix
                        if line.startswith(b'data: '):
                            line = line[6:]
                            
                            # Check for done signal
                            if line == b'[DONE]':
                                continue
                            
                            try:
                                # Handle potential UTF-8 decoding errors
                                try:
                                    line_str = line.decode('utf-8')
                                except UnicodeDecodeError:
                                    # Try with error handling
                                    line_str = line.decode('utf-8', errors='replace')
                                
                                chunk_data = json.loads(line_str)
                                
                                # Extract content if available
                                if 'choices' in chunk_data and chunk_data['choices']:
                                    choice = chunk_data['choices'][0]
                                    if 'delta' in choice and 'content' in choice['delta']:
                                        content_delta = choice['delta']['content']
                                        full_content += content_delta
                                        print(content_delta, end='', flush=True)
                                
                                # Extract usage if available
                                if 'usage' in chunk_data:
                                    usage = chunk_data['usage']
                            except json.JSONDecodeError:
                                pass
                            except Exception as e:
                                # Ignore other errors to keep streaming going
                                pass
        except HTTPError as e:
            # Read error response
            error_content = e.read().decode('utf-8')
            raise Exception(f"HTTP Error {e.code}: {e.reason}\nResponse: {error_content}")
        except URLError as e:
            raise Exception(f"URL Error: {e.reason}")
        
        end_time = time.time()
        
        # Calculate statistics
        elapsed_time = end_time - start_time
        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)
        total_tokens = usage.get('total_tokens', 0)
        
        # Calculate tokens per second
        tokens_per_second = completion_tokens / elapsed_time if elapsed_time > 0 else 0
        
        return {
            'content': full_content,
            'usage': usage,
            'statistics': {
                'elapsed_time': elapsed_time,
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': total_tokens,
                'tokens_per_second': tokens_per_second
            }
        }


def main():
    """Main function for interactive chat"""
    print("=== Interactive LLM Chat ===")
    print("Type your message and press Enter to send")
    print("Press Ctrl+C to exit\n")
    
    try:
        client = LLMClient()
        print(f"Connected to: {client.model}")
        print(f"Base URL: {client.base_url}\n")
        
        # Initialize chat history
        chat_history = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            }
        ]
        
        while True:
            # Get user input
            try:
                user_input = input("You: ")
                if not user_input.strip():
                    continue
            except KeyboardInterrupt:
                print("\nExiting chat...")
                break
            
            # Add user message to history
            chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Send request and stream response
            print("AI: ", end='', flush=True)
            
            try:
                result = client.chat_stream(chat_history)
                
                # Add assistant response to history
                chat_history.append({
                    "role": "assistant",
                    "content": result['content']
                })
                
                # Print statistics
                print("\n")
                stats = result['statistics']
                print(f"[Stats] Time: {stats['elapsed_time']:.2f}s, Tokens: {stats['total_tokens']}, Speed: {stats['tokens_per_second']:.2f} tokens/s")
                print("=" * 50)
                
            except Exception as e:
                print(f"\nError: {e}")
                print("=" * 50)
                
                # Remove the last user message from history to allow retrying
                if len(chat_history) > 1:
                    chat_history.pop()
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
