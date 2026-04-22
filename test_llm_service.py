#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import subprocess
import json
import os

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
env_vars = {}

if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

# Get LLM configuration
base_url = env_vars.get('LLM_BASE_URL', 'http://127.0.0.1:1234')
model = env_vars.get('LLM_MODEL', 'qwen/qwen3.5-9b')
api_key = env_vars.get('LLM_API_KEY', '123456')

# Ensure base_url ends with /v1 if not already present
if not base_url.endswith('/v1'):
    base_url = base_url.rstrip('/') + '/v1'

url = f"{base_url}/chat/completions"

# Prepare request data
data = {
    "model": model,
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant"
        },
        {
            "role": "user",
            "content": "Hello, how are you?"
        }
    ],
    "temperature": 1,
    "max_tokens": 100,
    "stream": False
}

# Convert data to JSON
json_data = json.dumps(data, ensure_ascii=False)

# Prepare curl command
cmd = [
    'curl',
    '-X', 'POST',
    '-H', 'Content-Type: application/json',
    '-H', f'Authorization: Bearer {api_key}',
    '-d', json_data,
    url
]

print(f"Testing LLM service at: {url}")
print(f"Using model: {model}")
print(f"Request data: {json_data[:500]}...")
print()
print("Running curl command...")
print(' '.join(cmd))
print()

# Run curl command
result = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    encoding='utf-8'
)

print("Return code:", result.returncode)
print()
print("STDOUT:")
print(result.stdout)
print()
print("STDERR:")
print(result.stderr)

if result.returncode == 0:
    try:
        response_data = json.loads(result.stdout)
        print()
        print("Parsed response:")
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print()
        print(f"Error parsing JSON response: {e}")
