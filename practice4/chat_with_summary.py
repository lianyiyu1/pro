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
        
        # Send request with retry for 429 errors
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            req = Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
            
            try:
                with urlopen(req, timeout=10) as response:
                    response_content = response.read().decode('utf-8', errors='replace')
                    response_data = json.loads(response_content)
                    
                    # Extract message and content
                    if 'choices' in response_data and response_data['choices']:
                        message = response_data['choices'][0]['message']
                        content = message.get('content', '')
                    else:
                        content = ''
                        message = {}
                    
                    # Extract usage
                    usage = response_data.get('usage', {})
                break  # Success, exit retry loop
            except HTTPError as e:
                # Read error response
                error_content = e.read().decode('utf-8')
                
                # Handle 429 Too Many Requests error with retry
                if e.code == 429 and attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    raise Exception(f"HTTP Error {e.code}: {e.reason}\nResponse: {error_content}")
            except URLError as e:
                raise Exception(f"URL Error: {e.reason}")
            except Exception as e:
                raise
        
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
        import json
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
        elif tool_name == "search_chat_history":
            query = arguments.get('query', '')
            log_file = r"D:\chat-log\log.txt"
            
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                result = {"content": content, "query": query}
            else:
                result = {"error": "Chat history log file not found"}
        elif tool_name == "anythingllm_query":
            query = arguments.get('query', '')
            env = load_env()
            api_key = env.get('ANYTHINGLLM_API_KEY')
            workspace_slug = env.get('ANYTHINGLLM_WORKSPACE_SLUG')
            
            if not api_key or not workspace_slug:
                result = {"error": "Missing ANYTHINGLLM_API_KEY or ANYTHINGLLM_WORKSPACE_SLUG in .env file"}
            else:
                import subprocess
                
                url = f"http://localhost:3001/api/v1/workspace/{workspace_slug}/chat"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                }
                
                data = {
                    'message': query
                }
                
                try:
                    # Use curl command to make the request
                    cmd = [
                        'curl',
                        '-X', 'POST',
                        '-H', f'Content-Type: application/json',
                        '-H', f'Authorization: Bearer {api_key}',
                        '-d', json.dumps(data, ensure_ascii=False),
                        url
                    ]
                    
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        encoding='utf-8'
                    )
                    
                    if result.returncode == 0:
                        try:
                            response_data = json.loads(result.stdout)
                            result = {"response": response_data}
                        except json.JSONDecodeError:
                            result = {"response": result.stdout}
                    else:
                        result = {"error": f"Curl error: {result.stderr}"}
                except Exception as e:
                    result = {"error": str(e)}
        else:
            result = {"error": f"Unknown tool: {tool_name}"}
        
        print(f"Tool execution result: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        error_result = {"error": str(e)}
        print(f"Tool execution error: {error_result}")
        return error_result


def get_chat_context_length(messages):
    """Calculate the total length of chat context"""
    total_length = 0
    for message in messages:
        if 'content' in message:
            total_length += len(message['content'])
    return total_length


def generate_chat_summary(messages, client):
    """Generate a summary of chat history"""
    # Prepare summary prompt
    summary_prompt = """
    Please summarize the following chat history concisely. Focus on the key points, important information, and main topics discussed.
    The summary should be brief but comprehensive, capturing the essence of the conversation.
    
    Chat History:
    """
    
    # Extract user and assistant messages (excluding system and tool messages)
    relevant_messages = []
    for message in messages:
        if message['role'] in ['user', 'assistant']:
            relevant_messages.append(f"{message['role'].capitalize()}: {message['content']}")
    
    # Create summary request
    summary_messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that summarizes chat history. Keep the summary concise and focused, only providing the core content without unnecessary paragraph markers, special symbols, or English text when summarizing Chinese conversations. Avoid excessive formatting and focus on capturing the essence of the conversation."
        },
        {
            "role": "user",
            "content": summary_prompt + "\n".join(relevant_messages)
        }
    ]
    
    # Get summary from LLM
    print("\n=== Generating chat summary ===")
    summary_result = client.chat(summary_messages)
    summary = summary_result['content']
    print(f"=== Summary generated ===\n{summary}\n")
    
    return summary


def compress_chat_history(messages):
    """Compress chat history by summarizing the first 70% and keeping the last 30% as original"""
    # Filter out system messages (keep only user and assistant messages for compression)
    user_assistant_messages = []
    system_messages = []
    
    for message in messages:
        if message['role'] == 'system':
            system_messages.append(message)
        else:
            user_assistant_messages.append(message)
    
    if len(user_assistant_messages) <= 1:
        return messages
    
    # Calculate split point (70% for summary, 30% for original)
    split_index = int(len(user_assistant_messages) * 0.7)
    
    # Split messages
    messages_to_summarize = user_assistant_messages[:split_index]
    messages_to_keep = user_assistant_messages[split_index:]
    
    # Create compressed history
    compressed_history = system_messages.copy()
    
    # Add summary as a single message
    if messages_to_summarize:
        summary_content = "[Chat Summary] "
        # Simple summary placeholder (will be replaced by actual LLM summary)
        summary_content += "This is a summary of the previous conversation."
        compressed_history.append({
            "role": "assistant",
            "content": summary_content
        })
    
    # Add the last 30% of messages as original
    compressed_history.extend(messages_to_keep)
    
    return compressed_history


def extract_key_information(messages, client):
    """Extract key information from chat history using 5W rules"""
    # Prepare extraction prompt
    extraction_prompt = """
    Please extract key information from the following chat history using the 5W rules:
    - Who: Who is involved
    - What: What happened
    - When: When did it happen (optional)
    - Where: Where did it happen (optional)
    - Why: Why did it happen (optional)
    
    Extract multiple key information points if applicable. Format each point as:
    [Who] [What] [When] [Where] [Why]
    
    Chat History:
    """
    
    # Extract user and assistant messages (excluding system and tool messages)
    relevant_messages = []
    for message in messages:
        if message['role'] in ['user', 'assistant']:
            relevant_messages.append(f"{message['role'].capitalize()}: {message['content']}")
    
    # Create extraction request
    extraction_messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that extracts key information from chat history using the 5W rules. Extract multiple key information points if applicable and format each point clearly."
        },
        {
            "role": "user",
            "content": extraction_prompt + "\n".join(relevant_messages)
        }
    ]
    
    # Get extraction result from LLM
    print("\n=== Extracting key information ===")
    extraction_result = client.chat(extraction_messages)
    extracted_info = extraction_result['content']
    print(f"=== Key information extracted ===\n{extracted_info}\n")
    
    return extracted_info


def save_key_information(info):
    r"""Save extracted key information to D:\chat-log\log.txt"""
    log_dir = r"D:\chat-log"
    log_file = os.path.join(log_dir, "log.txt")
    
    # Create directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Created directory: {log_dir}")
    
    # Append to file
    with open(log_file, 'a', encoding='utf-8') as f:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n=== Extracted at {timestamp} ===\n")
        f.write(info)
        f.write("\n")
    
    print(f"Key information saved to: {log_file}")


def main():
    """Main function for interactive chat with tool calling and chat history summarization"""
    print("=== Interactive LLM Chat with Tool Calling and History Summary ===")
    print("Type your message and press Enter to send")
    print("Press Ctrl+C to exit\n")
    
    try:
        client = LLMClient()
        print(f"Connected to: {client.model}")
        print(f"Base URL: {client.base_url}\n")
        
        # Get current date
        current_date = time.strftime('%Y-%m-%d')
        
        # System prompt with tool descriptions and current date
        system_prompt = "You are a helpful AI assistant with access to the following tools:\n"
        system_prompt += "1. list_files(directory: str)\n"
        system_prompt += "   - 列出某个目录下有哪些文件（包括文件的基本属性、大小等信息）\n"
        system_prompt += "   - 参数: directory (目录路径)\n"
        system_prompt += "2. rename_file(directory: str, old_name: str, new_name: str)\n"
        system_prompt += "   - 修改某个目录下某个文件的名字\n"
        system_prompt += "   - 参数: directory (目录路径), old_name (旧文件名), new_name (新文件名)\n"
        system_prompt += "3. delete_file(directory: str, filename: str)\n"
        system_prompt += "   - 删除某个目录下的某个文件\n"
        system_prompt += "   - 参数: directory (目录路径), filename (文件名)\n"
        system_prompt += "4. create_file(directory: str, filename: str, content: str)\n"
        system_prompt += "   - 在某个目录下新建1个文件，并且写入内容\n"
        system_prompt += "   - 参数: directory (目录路径), filename (文件名), content (文件内容)\n"
        system_prompt += "5. read_file(directory: str, filename: str)\n"
        system_prompt += "   - 读取某个目录下的某个文件的内容\n"
        system_prompt += "   - 参数: directory (目录路径), filename (文件名)\n"
        system_prompt += "6. curl(url: str, timeout: int = 30)\n"
        system_prompt += "   - 通过curl访问网页并返回网页内容，可用于获取实时信息如天气、新闻等\n"
        system_prompt += "   - 参数: url (网页URL), timeout (超时时间，默认30秒)\n"
        system_prompt += "   - 示例: 要获取天气信息，可以访问天气网站的URL\n"
        system_prompt += "7. search_chat_history(query: str)\n"
        system_prompt += "   - 查找聊天历史中的信息\n"
        system_prompt += "   - 参数: query (查询关键词)\n"
        system_prompt += "8. anythingllm_query(query: str)\n"
        system_prompt += "   - 查询AnythingLLM文档仓库中的信息\n"
        system_prompt += "   - 参数: query (查询内容)\n"
        system_prompt += "   - 当用户提到\"文档仓库\"、\"文件仓库\"、\"仓库\"时使用此工具\n"
        system_prompt += "\nWhen you need to use a tool, format your response as:\n\n"
        system_prompt += "{\n"
        system_prompt += "  \"tool_call\": {\n"
        system_prompt += "    \"name\": \"tool_name\",\n"
        system_prompt += "    \"arguments\": {\n"
        system_prompt += "      \"parameter1\": \"value1\",\n"
        system_prompt += "      \"parameter2\": \"value2\"\n"
        system_prompt += "    }\n"
        system_prompt += "  }\n"
        system_prompt += "}\n\n"
        system_prompt += "After receiving the tool execution result, provide a natural language response to the user based on the result.\n\n"
        system_prompt += "If you can answer the user's question without using a tool, simply provide a direct answer.\n\n"
        system_prompt += "Important tool usage guidelines:\n"
        system_prompt += "1. For anythingllm_query tool: Always include the full user query in the 'query' parameter\n"
        system_prompt += "2. For search_chat_history tool: Always include the search keywords in the 'query' parameter\n"
        system_prompt += "3. For file operations: Always provide the complete directory path and filename\n"
        system_prompt += "4. For curl tool: Always provide a valid URL\n\n"
        system_prompt += "Important:\n"
        system_prompt += "1. Today's date is " + current_date + ". Use this date when answering questions that require current date information.\n"
        system_prompt += "2. You have FULL ABILITY to access the internet through the curl tool. When users ask for real-time information like weather, news, or other web-based content, you MUST use the curl tool to fetch the information.\n"
        system_prompt += "3. For weather queries, you can use weather websites like https://wttr.in/ or weather APIs to get current weather data.\n"
        system_prompt += "4. Always try to use the curl tool when users ask for information that requires internet access.\n"
        system_prompt += "5. You should NEVER say you cannot access the internet or real-time information. Instead, use the curl tool to get the information.\n"
        system_prompt += "6. When users ask about weather, news, or any other real-time information, immediately use the curl tool to fetch the data.\n"
        system_prompt += "7. Keep your responses concise and focused. Only provide the core content without unnecessary paragraph markers, special symbols, or English text when responding in Chinese.\n"
        system_prompt += "8. Avoid using excessive formatting, emojis, or decorative elements. Focus on providing clear, direct answers.\n"
        system_prompt += "9. When users send messages starting with \"/search\" or express the meaning of \"finding chat history\", use the search_chat_history tool.\n"
        system_prompt += "10. When you think you should find chat history to answer the user's question, use the search_chat_history tool.\n"
        system_prompt += "11. When users mention \"文档仓库\" (document repository), \"文件仓库\" (file repository), or \"仓库\" (repository), use the anythingllm_query tool.\n"
        system_prompt += "12. When you need to query information from the document repository, use the anythingllm_query tool.\n"
        
        # Initialize chat history
        chat_history = [
            {
                "role": "system",
                "content": system_prompt.strip()
            }
        ]
        
        # Track conversation rounds (count only user-assistant exchanges)
        conversation_rounds = 0
        
        while True:
            # Check if chat history needs summarization
            context_length = get_chat_context_length(chat_history)
            
            # Count actual conversation rounds (excluding system and tool messages)
            user_assistant_count = 0
            for message in chat_history:
                if message['role'] in ['user', 'assistant']:
                    user_assistant_count += 1
            
            # Each round consists of one user message and one assistant response
            current_rounds = user_assistant_count // 2
            
            # Check if we need to summarize
            if current_rounds >= 5 or (context_length > 5000 and current_rounds > 0):
                print("\n=== Chat history threshold reached, generating summary ===")
                print(f"Current conversation rounds: {current_rounds}")
                print(f"Current context length: {context_length}\n")
                
                # Extract and save key information
                key_info = extract_key_information(chat_history, client)
                save_key_information(key_info)
                
                # Compress chat history
                compressed_history = compress_chat_history(chat_history)
                
                # Generate actual summary for the first part
                summary = generate_chat_summary(chat_history, client)
                
                # Replace the placeholder summary with actual summary
                for i, message in enumerate(compressed_history):
                    if message['role'] == 'assistant' and message['content'].startswith('[Chat Summary]'):
                        compressed_history[i]['content'] = f"[Chat Summary] {summary}"
                        break
                
                # Update chat history with compressed version
                chat_history = compressed_history
                
                print("=== Chat history compressed ===")
                print(f"New context length: {get_chat_context_length(chat_history)}")
                print(f"New message count: {len(chat_history)}\n")
            
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
                print("=" * 70)
                
            except Exception as e:
                print(f"\nError: {e}")
                print("=" * 70)
                
                # Remove the last user message from history to allow retrying
                if len(chat_history) > 1:
                    chat_history.pop()
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()