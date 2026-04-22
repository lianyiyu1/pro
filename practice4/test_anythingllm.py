#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_with_summary import execute_tool

# Test the anythingllm_query tool
tool_call = {
    "name": "anythingllm_query",
    "arguments": {
        "query": "我的文档仓库上传了几个文档"
    }
}

print("Testing anythingllm_query tool...")
result = execute_tool(tool_call)
print(f"Tool execution result: {result}")
