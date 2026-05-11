#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
测试链式工具调用功能
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chat_with_chained_calls import LLMClient, execute_chained_tool_call

def test_search_chained_call():
    """测试1：文件搜索链式调用"""
    print("=" * 70)
    print("测试1：文件搜索链式调用")
    print("=" * 70)
    
    client = LLMClient()
    user_request = "请查找 practice05 目录下所有包含'def'关键词的文件，并总结这些文件的主要内容"
    
    print(f"用户请求: {user_request}")
    print()
    
    result = execute_chained_tool_call(client, user_request, max_iterations=10)
    
    print("\n" + "=" * 70)
    print(f"测试1完成，结果: {result}")
    print("=" * 70 + "\n")
    
    return result

def test_skill_chained_call():
    """测试2：技能查询链式调用"""
    print("=" * 70)
    print("测试2：技能查询链式调用")
    print("=" * 70)
    
    client = LLMClient()
    user_request = "我想了解 notice 技能的详细规则"
    
    print(f"用户请求: {user_request}")
    print()
    
    result = execute_chained_tool_call(client, user_request, max_iterations=10)
    
    print("\n" + "=" * 70)
    print(f"测试2完成，结果: {result}")
    print("=" * 70 + "\n")
    
    return result

def test_web_chained_call():
    """测试3：网页处理链式调用"""
    print("=" * 70)
    print("测试3：网页处理链式调用")
    print("=" * 70)
    
    client = LLMClient()
    user_request = "访问 https://www.nsu.edu.cn/HTML/news/2024/06/article_3974.html 并总结页面内容，保存到 practice06/summary.txt"
    
    print(f"用户请求: {user_request}")
    print()
    
    result = execute_chained_tool_call(client, user_request, max_iterations=10)
    
    print("\n" + "=" * 70)
    print(f"测试3完成，结果: {result}")
    print("=" * 70 + "\n")
    
    return result

def main():
    """运行所有测试"""
    print("=== 链式工具调用测试套件 ===")
    print()
    
    test_search_chained_call()
    test_skill_chained_call()
    test_web_chained_call()
    
    print("=== 所有测试完成 ===")

if __name__ == "__main__":
    main()