#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_with_summary import list_available_skills, load_skill_content
import json

# Test the skill functions
def test_skill_functions():
    print("Testing skill functions...")
    
    try:
        # Test list_available_skills
        print("\n=== Testing list_available_skills ===")
        skills = list_available_skills()
        print(f"Available skills: {json.dumps(skills, ensure_ascii=False)}")
        
        # Test load_skill_content
        print("\n=== Testing load_skill_content ===")
        skill_content = load_skill_content('notice')
        print(f"Notice skill content: {skill_content}")
        
        print("\nAll tests passed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_skill_functions()
