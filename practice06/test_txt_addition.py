#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
测试txt文件相加功能
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chat_with_chained_calls import LLMClient, execute_chained_tool_call

def test_txt_addition():
    """测试txt文件相加"""
    print("=" * 70)
    print("测试：txt文件相加")
    print("=" * 70)
    
    client = LLMClient()
    user_request = "practice06目录下的1.txt和2.txt文件，其中的数值均为整数，两数相加为多少"
    
    print(f"用户请求: {user_request}")
    print()
    
    result = execute_chained_tool_call(client, user_request, max_iterations=10)
    
    print("\n" + "=" * 70)
    print(f"测试完成，结果: {result}")
    print("=" * 70 + "\n")
    
    return result

if __name__ == "__main__":
    test_txt_addition()