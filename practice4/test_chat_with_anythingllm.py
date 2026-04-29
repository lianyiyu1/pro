#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
import os
import traceback

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Starting test script...")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

try:
    from chat_with_summary import LLMClient, execute_tool
    print("Successfully imported modules")
except Exception as e:
    print(f"Error importing modules: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test the complete chat flow with anythingllm_query
def test_chat_with_anythingllm():
    print("\nTesting chat with anythingllm_query tool...")
    
    try:
        # Initialize LLM client
        client = LLMClient()
        print(f"Connected to: {client.model}")
        print(f"Base URL: {client.base_url}")
        
        # Get current date
        import time
        current_date = time.strftime('%Y-%m-%d')
        print(f"Current date: {current_date}")
        
        # Create system prompt
        system_prompt = "You are a helpful AI assistant with access to the following tools:\n"
        system_prompt += "1. anythingllm_query(query: str)\n"
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
        system_prompt += "Important:\n"
        system_prompt += "1. Today's date is " + current_date + ". Use this date when answering questions that require current date information.\n"
        system_prompt += "2. When users mention \"文档仓库\" (document repository), \"文件仓库\" (file repository), or \"仓库\" (repository), use the anythingllm_query tool.\n"
        
        # Initialize chat history
        chat_history = [
            {
                "role": "system",
                "content": system_prompt.strip()
            }
        ]
        
        # Add user message
        user_message = input("YOU: ")
        chat_history.append({"role": "user", "content": user_message})
        
        # Get LLM response
        result = client.chat(chat_history)
        content = result['content']
        print("\nAI：", content)
        
        # Check if it's a tool call
        import json
        try:
            if content.strip().startswith('{'):
                tool_call_data = json.loads(content.strip())
                if 'tool_call' in tool_call_data:
                    tool_call = tool_call_data['tool_call']
                    print("\nExecuting tool call:", tool_call)
                    
                    # Execute the tool
                    tool_result = execute_tool(tool_call)
                    print("\nTool execution result:", json.dumps(tool_result, indent=2, ensure_ascii=False))
                    
                    # Add tool response to history
                    chat_history.append({"role": "assistant", "content": content})
                    chat_history.append({"role": "tool", "content": json.dumps(tool_result)})
                    
                    # Get LLM's response to tool result
                    print("\nGetting LLM response to tool result...")
                    tool_response = client.chat(chat_history)
                    tool_response_content = tool_response['content']
                    print("\nLLM response to tool result:", tool_response_content)
                    
                    print("\nTest completed successfully!")
                else:
                    print("\nNot a tool call response")
            else:
                print("\nNot a JSON response")
        except json.JSONDecodeError as e:
            print(f"\nInvalid JSON response: {e}")
        except Exception as e:
            print(f"\nError processing tool call: {e}")
            traceback.print_exc()
    except Exception as e:
        print(f"\nError in test function: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_chat_with_anythingllm()
