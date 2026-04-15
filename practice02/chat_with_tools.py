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
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from practice02.tools import list_files, rename_file, delete_file, create_file, read_file, curl


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
            'max_tokens': self.max_tokens,
            'stream': False  # Disable streaming for tool calls
        }
        
        # Send request
        req = Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        
        try:
            with urlopen(req) as response:
                response_content = response.read().decode('utf-8', errors='replace')
                response_data = json.loads(response_content)
                
                # Debug: print full response
                print("=== API Response ===")
                print(json.dumps(response_data, indent=2, ensure_ascii=False))
                print("====================")
                
                # Extract message and content
                if 'choices' in response_data and response_data['choices']:
                    message = response_data['choices'][0]['message']
                    content = message.get('content', '')
                else:
                    content = ''
                    message = {}
                
                # Extract usage
                usage = response_data.get('usage', {})
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
            'message': message,
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


def execute_tool(tool_call):
    """Execute tool call based on tool name and arguments"""
    try:
        tool_name = tool_call.get('name')
        arguments = tool_call.get('arguments', {})
        
        print(f"Executing tool: {tool_name}")
        print(f"Arguments: {json.dumps(arguments, indent=2)}")
        
        # Execute the appropriate tool
        if tool_name == "list_files":
            result = list_files(
                arguments.get('directory')
            )
        elif tool_name == "rename_file":
            result = rename_file(
                arguments.get('directory'),
                arguments.get('old_name'),
                arguments.get('new_name')
            )
        elif tool_name == "delete_file":
            result = delete_file(
                arguments.get('directory'),
                arguments.get('filename')
            )
        elif tool_name == "create_file":
            result = create_file(
                arguments.get('directory'),
                arguments.get('filename'),
                arguments.get('content')
            )
        elif tool_name == "read_file":
            result = read_file(
                arguments.get('directory'),
                arguments.get('filename')
            )
        elif tool_name == "curl":
            result = curl(
                arguments.get('url'),
                arguments.get('timeout', 30)
            )
        else:
            result = {"error": f"Unknown tool: {tool_name}"}
        
        print(f"Tool execution result: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        error_result = {"error": str(e)}
        print(f"Tool execution error: {error_result}")
        return error_result


def main():
    """Main function for interactive chat with tool calling"""
    print("=== Interactive LLM Chat with Tool Calling ===")
    print("Type your message and press Enter to send")
    print("Press Ctrl+C to exit\n")
    
    try:
        client = LLMClient()
        print(f"Connected to: {client.model}")
        print(f"Base URL: {client.base_url}\n")
        
        # Get current date
        current_date = time.strftime('%Y-%m-%d')
        
        # System prompt with tool descriptions and current date
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

When you need to use a tool, format your response as:

```json
{{
  "tool_call": {{
    "name": "tool_name",
    "arguments": {{
      "parameter1": "value1",
      "parameter2": "value2"
    }}
  }}
}}
```

After receiving the tool execution result, provide a natural language response to the user based on the result.

If you can answer the user's question without using a tool, simply provide a direct answer.

Important:
1. Today's date is {current_date}. Use this date when answering questions that require current date information.
2. You have FULL ABILITY to access the internet through the curl tool. When users ask for real-time information like weather, news, or other web-based content, you MUST use the curl tool to fetch the information.
3. For weather queries, you can use weather websites like https://wttr.in/ or weather APIs to get current weather data.
4. Always try to use the curl tool when users ask for information that requires internet access.
5. You should NEVER say you cannot access the internet or real-time information. Instead, use the curl tool to get the information.
6. When users ask about weather, news, or any other real-time information, immediately use the curl tool to fetch the data.
"""
        
        # Initialize chat history
        chat_history = [
            {
                "role": "system",
                "content": system_prompt.strip()
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
            
            # Send request to LLM
            print("AI: ", end='', flush=True)
            
            try:
                result = client.chat(chat_history)
                
                # Check if content exists and if it's a tool call
                content = result['content']
                
                if content:
                    # Try to parse tool call from content
                    try:
                        # Extract JSON from code blocks if present
                        if '```json' in content:
                            json_start = content.find('```json') + 7
                            json_end = content.find('```', json_start)
                            if json_end > json_start:
                                json_content = content[json_start:json_end].strip()
                                tool_call_data = json.loads(json_content)
                                if 'tool_call' in tool_call_data:
                                    tool_call = tool_call_data['tool_call']
                                    
                                    # Execute the tool
                                    tool_result = execute_tool(tool_call)
                                    
                                    # Add tool response to history
                                    chat_history.append({
                                        "role": "assistant",
                                        "content": content  # Original tool call
                                    })
                                    
                                    chat_history.append({
                                        "role": "tool",
                                        "content": json.dumps(tool_result)
                                    })
                                    
                                    # Get LLM's response to tool result
                                    print("\nAI: ", end='', flush=True)
                                    tool_response = client.chat(chat_history)
                                    tool_response_content = tool_response['content']
                                    print(tool_response_content)
                                    
                                    chat_history.append({
                                        "role": "assistant",
                                        "content": tool_response_content
                                    })
                                else:
                                    # Not a tool call, just display the content
                                    print(content)
                                    chat_history.append({
                                        "role": "assistant",
                                        "content": content
                                    })
                            else:
                                # No valid JSON block, just display the content
                                print(content)
                                chat_history.append({
                                    "role": "assistant",
                                    "content": content
                                })
                        else:
                            # No code block, check if it's a direct JSON object
                            if content.strip().startswith('{'):
                                tool_call_data = json.loads(content.strip())
                                if 'tool_call' in tool_call_data:
                                    tool_call = tool_call_data['tool_call']
                                    
                                    # Execute the tool
                                    tool_result = execute_tool(tool_call)
                                    
                                    # Add tool response to history
                                    chat_history.append({
                                        "role": "assistant",
                                        "content": content  # Original tool call
                                    })
                                    
                                    chat_history.append({
                                        "role": "tool",
                                        "content": json.dumps(tool_result)
                                    })
                                    
                                    # Get LLM's response to tool result
                                    print("\nAI: ", end='', flush=True)
                                    tool_response = client.chat(chat_history)
                                    tool_response_content = tool_response['content']
                                    print(tool_response_content)
                                    
                                    chat_history.append({
                                        "role": "assistant",
                                        "content": tool_response_content
                                    })
                                else:
                                    # Not a tool call, just display the content
                                    print(content)
                                    chat_history.append({
                                        "role": "assistant",
                                        "content": content
                                    })
                            else:
                                # Not a JSON object, just display the content
                                print(content)
                                chat_history.append({
                                    "role": "assistant",
                                    "content": content
                                })
                    except json.JSONDecodeError:
                        # Not a valid JSON, just display the content
                        print(content)
                        chat_history.append({
                            "role": "assistant",
                            "content": content
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
