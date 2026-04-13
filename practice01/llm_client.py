import os
import json
import time
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
    """OpenAI Compatible LLM Client using Python standard library"""
    
    def __init__(self):
        self.env = load_env()
        self.base_url = self.env.get('LLM_BASE_URL', 'http://127.0.0.1:1234/v1')
        self.model = self.env.get('LLM_MODEL', 'qwen/qwen3.5-9b')
        self.api_key = self.env.get('LLM_API_KEY', '123456')
        self.temperature = float(self.env.get('LLM_TEMPERATURE', '1'))
        self.max_tokens = int(self.env.get('LLM_MAX_TOKENS', '12146'))
        
        # Ensure base_url ends with /v1 if not already present
        if not self.base_url.endswith('/v1'):
            self.base_url = self.base_url.rstrip('/') + '/v1'
        
        if not all([self.base_url, self.model, self.api_key]):
            raise ValueError("Missing required LLM configuration in .env file")
    
    def chat(self, messages):
        """Send chat completion request to LLM"""
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
            'max_tokens': self.max_tokens
        }
        
        # Send request
        req = Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        
        try:
            with urlopen(req) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                
            # Debug: print full response
            print("=== API Response ===")
            print(json.dumps(response_data, indent=2))
            print("====================\n")
            
        except HTTPError as e:
            # Read error response
            error_content = e.read().decode('utf-8')
            raise Exception(f"HTTP Error {e.code}: {e.reason}\nResponse: {error_content}")
        except URLError as e:
            raise Exception(f"URL Error: {e.reason}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON Decode Error: {e}")
        
        end_time = time.time()
        
        # Check for error in response
        if 'error' in response_data:
            error_message = response_data['error']
            if isinstance(error_message, dict):
                error_message = error_message.get('message', str(error_message))
            raise Exception(f"API Error: {error_message}\n\nPossible solutions:\n1. Check if your local LLM service is running correctly\n2. Verify the API endpoint format\n3. Check your local LLM's documentation for the correct endpoint\n4. Ensure your LLM service supports OpenAI-compatible API")
        
        # Extract response with error handling
        if 'choices' not in response_data:
            raise Exception(f"Invalid response format: missing 'choices' field\nResponse: {json.dumps(response_data)}")
        
        if not response_data['choices']:
            raise Exception(f"Invalid response format: empty 'choices' array")
        
        if 'message' not in response_data['choices'][0]:
            raise Exception(f"Invalid response format: missing 'message' field")
        
        if 'content' not in response_data['choices'][0]['message']:
            raise Exception(f"Invalid response format: missing 'content' field")
        
        content = response_data['choices'][0]['message']['content']
        usage = response_data.get('usage', {})
        
        # Calculate statistics
        elapsed_time = end_time - start_time
        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)
        total_tokens = usage.get('total_tokens', 0)
        
        # Calculate tokens per second
        tokens_per_second = completion_tokens / elapsed_time if elapsed_time > 0 else 0
        
        return {
            'content': content,
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
    """Main function to demonstrate LLM usage"""
    print("=== LLM Client Demo ===\n")
    
    try:
        client = LLMClient()
        
        # Example conversation
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": "我叫什么名字"
            }
        ]
        
        print("Sending request to LLM...")
        print(f"Model: {client.model}")
        print(f"Base URL: {client.base_url}\n")
        
        result = client.chat(messages)
        
        print("=== Response ===")
        print(f"Content:\n{result['content']}\n")
        
        print("=== Usage Statistics ===")
        stats = result['statistics']
        print(f"Elapsed Time: {stats['elapsed_time']:.2f} seconds")
        print(f"Prompt Tokens: {stats['prompt_tokens']}")
        print(f"Completion Tokens: {stats['completion_tokens']}")
        print(f"Total Tokens: {stats['total_tokens']}")
        print(f"Tokens per Second: {stats['tokens_per_second']:.2f}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
