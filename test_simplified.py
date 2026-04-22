#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import os
import json
import time
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Import tools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from practice02.tools import list_files, rename_file, delete_file, create_file, read_file, curl

def load_env():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
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
    """OpenAI Compatible LLM Client"""
    
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

def main():
    """Simplified main function for testing"""
    print("=== Simplified Test ===")
    print("Initializing...")
    
    try:
        print("Loading environment...")
        env = load_env()
        print("Environment loaded successfully")
        
        print("Initializing LLM client...")
        client = LLMClient()
        print(f"Connected to: {client.model}")
        print(f"Base URL: {client.base_url}")
        
        print("Getting current date...")
        current_date = time.strftime('%Y-%m-%d')
        print(f"Current date: {current_date}")
        
        print("Creating system prompt...")
        system_prompt = f"""
You are a helpful AI assistant with access to the following tools:

1. list_files(directory: str)
   - 列出某个目录下有哪些文件（包括文件的基本属性、大小等信息）
   - 参数: directory (目录路径)

2. rename_file(directory: str, old_name: str, new_name: str)
   - 修改某个目录下某个文件的名字
   - 参数: directory (目录路径), old_name (旧文件名), new_name (新文件名)

3. delete_file(directory: str, filename: str)
   - 删除某个目录下的某个文件
   - 参数: directory (目录路径), filename (文件名)

4. create_file(directory: str, filename: str, content: str)
   - 在某个目录下新建1个文件，并且写入内容
   - 参数: directory (目录路径), filename (文件名), content (文件内容)

5. read_file(directory: str, filename: str)
   - 读取某个目录下的某个文件的内容
   - 参数: directory (目录路径), filename (文件名)

6. curl(url: str, timeout: int = 30)
   - 通过curl访问网页并返回网页内容，可用于获取实时信息如天气、新闻等
   - 参数: url (网页URL), timeout (超时时间，默认30秒)
   - 示例: 要获取天气信息，可以访问天气网站的URL

7. search_chat_history(query: str)
   - 查找聊天历史中的信息
   - 参数: query (查询关键词)

8. anythingllm_query(query: str)
   - 查询AnythingLLM文档仓库中的信息
   - 参数: query (查询内容)
   - 当用户提到"文档仓库"、"文件仓库"、"仓库"时使用此工具

When you need to use a tool, format your response as:

{{
  "tool_call": {{
    "name": "tool_name",
    "arguments": {{
      "parameter1": "value1",
      "parameter2": "value2"
    }}
  }}
}}

After receiving the tool execution result, provide a natural language response to the user based on the result.

If you can answer the user's question without using a tool, simply provide a direct answer.

Important:
1. Today's date is {current_date}. Use this date when answering questions that require current date information.
2. You have FULL ABILITY to access the internet through the curl tool. When users ask for real-time information like weather, news, or other web-based content, you MUST use the curl tool to fetch the information.
"""
        
        print("System prompt created successfully")
        print(f"System prompt length: {len(system_prompt)}")
        print("First 200 characters:")
        print(system_prompt[:200])
        print("...")
        
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
