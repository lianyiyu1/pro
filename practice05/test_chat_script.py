#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_with_summary import LLMClient, list_available_skills
import json
import time

# Test the chat script functionality
def test_chat_script():
    print("Testing chat script functionality...")
    
    try:
        # Initialize LLM client
        client = LLMClient()
        print(f"Connected to: {client.model}")
        print(f"Base URL: {client.base_url}")
        
        # Read available skills
        skills = list_available_skills()
        skills_json = json.dumps({"skills": skills}, ensure_ascii=False)
        print(f"Available skills: {skills_json}")
        
        # Get current date
        current_date = time.strftime('%Y-%m-%d')
        
        # System prompt with minimal information
        system_prompt = "You are a helpful AI assistant.\n"
        system_prompt += "\nAvailable skills:\n"
        system_prompt += skills_json + "\n\n"
        system_prompt += f"Today's date is {current_date}.\n"
        system_prompt += "When users ask to write, modify, or polish a notice, use the 'notice' skill.\n"
        system_prompt += "Notice skill rules:\n"
        system_prompt += "1. 开头必须是\"XX部通知\"或\"[部门]通知\"，不能直接写\"通知\"。\n"
        system_prompt += "2. 内容简洁、正式，包含事由、时间、要求。\n"
        system_prompt += "3. 用户未提供部门时，统一用\"XX部\"。\n"
        
        # Test case: User with learning department
        chat_history = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": "学习部的五一放假通知"
            }
        ]
        
        # Get LLM response
        print("\nUser: 学习部的五一放假通知")
        print("AI: ", end='', flush=True)
        
        start_time = time.time()
        result = client.chat(chat_history)
        end_time = time.time()
        
        content = result['content']
        print(content)
        
        # Print statistics
        print("\n")
        stats = result['statistics']
        print(f"[Stats] Time: {stats['elapsed_time']:.2f}s, Tokens: {stats['total_tokens']}, Speed: {stats['tokens_per_second']:.2f} tokens/s")
        print("=" * 70)
        
        # Check if response starts with "学习部通知"
        if "学习部通知" in content:
            print("Test passed: Response starts with '学习部通知'")
        else:
            print("Test failed: Response does not start with '学习部通知'")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chat_script()
