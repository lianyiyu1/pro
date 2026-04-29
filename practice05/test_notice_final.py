#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
import os
import time

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_with_summary import LLMClient, list_available_skills, load_skill_content
import json

# Test the notice skill with learning department
def test_learning_department_notice():
    print("Testing notice skill with learning department...")
    
    try:
        # Initialize LLM client
        print("Initializing LLM client...")
        start_time = time.time()
        client = LLMClient()
        end_time = time.time()
        print(f"LLM client initialized in {end_time - start_time:.2f} seconds")
        print(f"Connected to: {client.model}")
        print(f"Base URL: {client.base_url}")
        
        # Read available skills
        print("\nReading available skills...")
        start_time = time.time()
        skills = list_available_skills()
        end_time = time.time()
        print(f"Skills read in {end_time - start_time:.2f} seconds")
        print(f"Available skills: {json.dumps(skills, ensure_ascii=False)}")
        
        # Create chat history with system prompt
        system_prompt = "You are a helpful AI assistant.\n"
        system_prompt += "\nAvailable skills:\n"
        system_prompt += json.dumps({"skills": skills}, ensure_ascii=False) + "\n\n"
        system_prompt += f"Today's date is {time.strftime('%Y-%m-%d')}.\n"
        system_prompt += "When users ask to write, modify, or polish a notice, use the 'notice' skill.\n"
        system_prompt += "Notice skill rules:\n"
        system_prompt += "1. 开头必须是\"XX部通知\"或\"[部门]通知\"，不能直接写\"通知\"。\n"
        system_prompt += "2. 内容简洁、正式，包含事由、时间、要求。\n"
        system_prompt += "3. 用户未提供部门时，统一用\"XX部\"。\n"
        
        print(f"System prompt length: {len(system_prompt)}")
        
        # Test case 1: User without department
        print("\n=== Test 1: User without department ===")
        chat_history1 = [
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
        print("Waiting for LLM response...")
        start_time = time.time()
        
        result1 = client.chat(chat_history1)
        end_time = time.time()
        print(f"LLM response received in {end_time - start_time:.2f} seconds")
        
        response_content1 = result1['content']
        
        print("\nLLM response:")
        print(response_content1)
        
        # Check if response starts with "XX部通知"
        if "XX部通知" in response_content1:
            print("Test passed: Response starts with 'XX部通知'")
        else:
            print("Test failed: Response does not start with 'XX部通知'")
        
        # Test case 2: User with department
        print("\n=== Test 2: User with department ===")
        chat_history2 = [
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
        print("Waiting for LLM response...")
        start_time = time.time()
        
        result2 = client.chat(chat_history2)
        end_time = time.time()
        print(f"LLM response received in {end_time - start_time:.2f} seconds")
        
        response_content2 = result2['content']
        
        print("\nLLM response:")
        print(response_content2)
        
        # Check if response starts with "销售部通知"
        if "销售部通知" in response_content2:
            print("Test passed: Response starts with '销售部通知'")
        else:
            print("Test failed: Response does not start with '销售部通知'")
        
        # Test case 3: User with learning department
        print("\n=== Test 3: User with learning department ===")
        chat_history3 = [
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
        print("Sending request: 学习部的五一放假通知")
        print("Waiting for LLM response...")
        start_time = time.time()
        
        result3 = client.chat(chat_history3)
        end_time = time.time()
        print(f"LLM response received in {end_time - start_time:.2f} seconds")
        
        response_content3 = result3['content']
        
        print("\nLLM response:")
        print(response_content3)
        
        # Check if response starts with "学习部通知"
        if "学习部通知" in response_content3:
            print("Test passed: Response starts with '学习部通知'")
        else:
            print("Test failed: Response does not start with '学习部通知'")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_learning_department_notice()
