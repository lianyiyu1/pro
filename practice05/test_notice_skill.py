#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_with_summary import LLMClient, list_available_skills, load_skill_content
import json

# Test the notice skill functionality
def test_notice_skill():
    print("Testing notice skill functionality...")
    
    try:
        # Initialize LLM client
        client = LLMClient()
        print(f"Connected to: {client.model}")
        print(f"Base URL: {client.base_url}")
        
        # Read available skills
        skills = list_available_skills()
        print(f"Available skills: {json.dumps(skills, ensure_ascii=False)}")
        
        # Test 1: User without department
        print("\n=== Test 1: User without department ===")
        test_without_department(client, skills)
        
        # Test 2: User with department
        print("\n=== Test 2: User with department ===")
        test_with_department(client, skills)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

# Test case 1: User without department
def test_without_department(client, skills):
    # Create chat history with system prompt
    system_prompt = "You are a helpful AI assistant with access to the following skills:\n"
    system_prompt += json.dumps({"skills": skills}, ensure_ascii=False) + "\n\n"
    system_prompt += "When users ask to write, modify, or polish a notice, use the 'notice' skill."
    
    # Load notice skill content
    notice_skill_content = load_skill_content('notice')
    if notice_skill_content:
        system_prompt += "\n\nNotice skill content:\n" + notice_skill_content
    
    chat_history = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "撰写关于五一节放假的通知"
        }
    ]
    
    # Get LLM response
    print("Sending request: 撰写关于五一节放假的通知")
    result = client.chat(chat_history)
    response_content = result['content']
    
    print("LLM response:")
    print(response_content)
    
    # Check if response starts with "XX部通知"
    if "XX部通知" in response_content:
        print("✓ Test passed: Response starts with 'XX部通知'")
    else:
        print("✗ Test failed: Response does not start with 'XX部通知'")

# Test case 2: User with department
def test_with_department(client, skills):
    # Create chat history with system prompt
    system_prompt = "You are a helpful AI assistant with access to the following skills:\n"
    system_prompt += json.dumps({"skills": skills}, ensure_ascii=False) + "\n\n"
    system_prompt += "When users ask to write, modify, or polish a notice, use the 'notice' skill."
    
    # Load notice skill content
    notice_skill_content = load_skill_content('notice')
    if notice_skill_content:
        system_prompt += "\n\nNotice skill content:\n" + notice_skill_content
    
    chat_history = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "我是销售部的，撰写关于五一节放假的通知"
        }
    ]
    
    # Get LLM response
    print("Sending request: 我是销售部的，撰写关于五一节放假的通知")
    result = client.chat(chat_history)
    response_content = result['content']
    
    print("LLM response:")
    print(response_content)
    
    # Check if response starts with "销售部通知"
    if "销售部通知" in response_content:
        print("✓ Test passed: Response starts with '销售部通知'")
    else:
        print("✗ Test failed: Response does not start with '销售部通知'")

if __name__ == "__main__":
    test_notice_skill()
