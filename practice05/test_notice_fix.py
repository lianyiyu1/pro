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
        system_prompt = "You are a helpful AI assistant with access to the following skills:\n"
        system_prompt += json.dumps({"skills": skills}, ensure_ascii=False) + "\n\n"
        system_prompt += "When users ask to write, modify, or polish a notice, use the 'notice' skill."
        
        # Load notice skill content
        print("\nLoading notice skill content...")
        start_time = time.time()
        notice_skill_content = load_skill_content('notice')
        end_time = time.time()
        print(f"Notice skill content loaded in {end_time - start_time:.2f} seconds")
        if notice_skill_content:
            system_prompt += "\n\nNotice skill content:\n" + notice_skill_content
        
        print(f"System prompt length: {len(system_prompt)}")
        
        # Test case: User from learning department
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
        print("\nSending request: 学习部的五一放假通知")
        print("Waiting for LLM response...")
        start_time = time.time()
        
        # Add timeout parameter to chat method
        result = client.chat(chat_history)
        end_time = time.time()
        print(f"LLM response received in {end_time - start_time:.2f} seconds")
        
        response_content = result['content']
        
        print("\nLLM response:")
        print(response_content)
        
        # Check if response starts with "学习部通知"
        if "学习部通知" in response_content:
            print("✓ Test passed: Response starts with '学习部通知'")
        else:
            print("✗ Test failed: Response does not start with '学习部通知'")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_learning_department_notice()
