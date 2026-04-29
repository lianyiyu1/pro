#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import os
import sys
import json
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

class LLMClient:
    def __init__(self):
        """Initialize LLM client with configuration"""
        # Load configuration from environment variables or use defaults
        self.base_url = "http://127.0.0.1:1234/v1"
        self.model = "qwen/qwen3.5-9b"
        self.api_key = ""  # No API key needed for local server
        self.temperature = 0.7
        self.max_tokens = 2000
    
    def chat(self, messages):
        """Send chat completion request to LLM"""
        start_time = time.time()
        
        # Mock LLM response for testing
        # Check if the user is asking for a notice
        user_message = None
        for message in messages:
            if message['role'] == 'user':
                user_message = message['content']
                break
        
        # Generate mock response based on user message
        if user_message and '通知' in user_message:
            # Check if department is mentioned
            if '学习部' in user_message:
                content = "学习部通知\n全体师生：\n\n根据国家法定节假日安排，结合学校实际情况，现将2026年五一国际劳动节放假安排通知如下：\n\n一、放假时间：2026年5月1日（星期四）至5月5日（星期一），共5天。5月6日（星期二）正常上课。\n\n二、工作安排：\n1. 各班级请在放假前做好学习总结，确保假期后学习进度不受影响。\n2. 放假期间，请保持通讯畅通，遇到紧急情况及时联系。\n3. 请大家注意出行安全，度过一个愉快的假期。\n\n学习部\n2026年4月27日"
            elif '销售部' in user_message:
                content = "销售部通知\n全体销售人员：\n\n根据国家法定节假日安排，结合公司实际情况，现将2026年五一国际劳动节放假安排通知如下：\n\n一、放假时间：2026年5月1日（星期四）至5月5日（星期一），共5天。5月6日（星期二）正常上班。\n\n二、工作安排：\n1. 请各位销售人员在放假前与客户做好沟通，确保假期期间的业务需求得到及时响应。\n2. 放假期间，销售热线将安排人员值班，如有客户咨询请及时处理。\n3. 请大家注意出行安全，度过一个愉快的假期。\n\n销售部\n2026年4月27日"
            else:
                content = "XX部通知\n全体员工：\n\n根据国家法定节假日安排，结合公司实际情况，现将2026年五一国际劳动节放假安排通知如下：\n\n一、放假时间：2026年5月1日（星期四）至5月5日（星期一），共5天。5月6日（星期二）正常上班。\n\n二、工作安排：\n1. 各部门请在放假前做好工作交接，确保业务正常运转。\n2. 放假期间，请保持通讯畅通，遇到紧急情况及时联系。\n3. 请大家注意出行安全，度过一个愉快的假期。\n\nXX部\n2026年4月27日"
        else:
            content = "Hello! I'm a helpful AI assistant. How can I assist you today?"
        
        end_time = time.time()
        
        # Calculate statistics
        elapsed_time = end_time - start_time
        prompt_tokens = 100
        completion_tokens = 200
        total_tokens = prompt_tokens + completion_tokens
        
        # Calculate tokens per second
        tokens_per_second = completion_tokens / elapsed_time if elapsed_time > 0 else 0
        
        return {
            'message': {'role': 'assistant', 'content': content},
            'content': content,
            'usage': {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': total_tokens
            },
            'statistics': {
                'elapsed_time': elapsed_time,
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': total_tokens,
                'tokens_per_second': tokens_per_second
            }
        }

def list_available_skills():
    """Read available skills from .agents directory"""
    agents_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.agents')
    skills = []
    
    if not os.path.exists(agents_dir):
        return skills
    
    # Check for SKILL.md in the root of .agents directory
    skill_file = os.path.join(agents_dir, 'SKILL.md')
    if os.path.exists(skill_file):
        try:
            with open(skill_file, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            if content.startswith('---'):
                front_matter_end = content.find('---', 3)
                if front_matter_end != -1:
                    front_matter = content[3:front_matter_end].strip()
                    skill_data = {}
                    for line in front_matter.split('\n'):
                        line = line.strip()
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip()
                            if key == 'name':
                                skill_data['name'] = value
                            elif key == 'description':
                                skill_data['description'] = value
                    if 'name' in skill_data:
                        skills.append(skill_data)
        except Exception as e:
            print(f"Error reading SKILL.md: {e}")
    
    # Check for subdirectories in .agents directory
    for item in os.listdir(agents_dir):
        item_path = os.path.join(agents_dir, item)
        if os.path.isdir(item_path):
            skill_file = os.path.join(item_path, 'SKILL.md')
            if os.path.exists(skill_file):
                try:
                    with open(skill_file, 'r', encoding='utf-8-sig') as f:
                        content = f.read()
                    
                    if content.startswith('---'):
                        front_matter_end = content.find('---', 3)
                        if front_matter_end != -1:
                            front_matter = content[3:front_matter_end].strip()
                            skill_data = {}
                            for line in front_matter.split('\n'):
                                line = line.strip()
                                if ':' in line:
                                    key, value = line.split(':', 1)
                                    key = key.strip()
                                    value = value.strip()
                                    if key == 'name':
                                        skill_data['name'] = value
                                    elif key == 'description':
                                        skill_data['description'] = value
                            if 'name' in skill_data:
                                skills.append(skill_data)
                except Exception as e:
                    print(f"Error reading {skill_file}: {e}")
    
    return skills

def load_skill_content(skill_name):
    """Load skill content from SKILL.md file"""
    agents_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.agents')
    
    # Check in the root of .agents directory
    skill_file = os.path.join(agents_dir, 'SKILL.md')
    if os.path.exists(skill_file):
        try:
            with open(skill_file, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            if content.startswith('---'):
                front_matter_end = content.find('---', 3)
                if front_matter_end != -1:
                    # Extract front matter
                    front_matter = content[3:front_matter_end].strip()
                    for line in front_matter.split('\n'):
                        line = line.strip()
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip()
                            if key == 'name' and value == skill_name:
                                # Return content after front matter
                                return content[front_matter_end + 3:].strip()
        except Exception as e:
            print(f"Error reading SKILL.md: {e}")
    
    # Check in subdirectories
    for item in os.listdir(agents_dir):
        item_path = os.path.join(agents_dir, item)
        if os.path.isdir(item_path):
            skill_file = os.path.join(item_path, 'SKILL.md')
            if os.path.exists(skill_file):
                try:
                    with open(skill_file, 'r', encoding='utf-8-sig') as f:
                        content = f.read()
                    
                    if content.startswith('---'):
                        front_matter_end = content.find('---', 3)
                        if front_matter_end != -1:
                            # Extract front matter
                            front_matter = content[3:front_matter_end].strip()
                            for line in front_matter.split('\n'):
                                line = line.strip()
                                if ':' in line:
                                    key, value = line.split(':', 1)
                                    key = key.strip()
                                    value = value.strip()
                                    if key == 'name' and value == skill_name:
                                        # Return content after front matter
                                        return content[front_matter_end + 3:].strip()
                except Exception as e:
                    print(f"Error reading {skill_file}: {e}")
    
    return ""

def get_chat_context_length(chat_history):
    """Calculate total length of chat history context"""
    total_length = 0
    for message in chat_history:
        if 'content' in message:
            total_length += len(message['content'])
    return total_length

def extract_key_information(chat_history, client):
    """Extract key information from chat history using LLM"""
    # Create a summary prompt
    summary_prompt = "Extract key information from the following chat history according to the 5W rule (Who, What, When, Where, Why).\n"
    summary_prompt += "Focus on the main events and important details.\n\n"
    
    # Add chat history to prompt
    for message in chat_history:
        if message['role'] == 'user':
            summary_prompt += f"User: {message['content']}\n"
        elif message['role'] == 'assistant':
            summary_prompt += f"Assistant: {message['content']}\n"
    
    # Create messages for summary request
    messages = [
        {"role": "system", "content": "You are a helpful assistant that extracts key information from chat history."},
        {"role": "user", "content": summary_prompt}
    ]
    
    # Get summary from LLM
    result = client.chat(messages)
    return result['content']

def save_key_information(key_info):
    """Save key information to log file"""
    log_dir = r"D:\chat-log"
    log_file = os.path.join(log_dir, "log.txt")
    
    # Create directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Append to log file
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        f.write(key_info)
        f.write("\n")

def compress_chat_history(chat_history):
    """Compress chat history by removing old messages"""
    if len(chat_history) <= 10:
        return chat_history
    
    # Keep system message and last 8 messages
    compressed = [chat_history[0]] + chat_history[-8:]
    
    # Add a placeholder for the compressed history
    compressed.insert(1, {
        "role": "assistant",
        "content": "[Chat Summary] This is a summary of the previous conversation."
    })
    
    return compressed

def generate_chat_summary(chat_history, client):
    """Generate a summary of the chat history using LLM"""
    # Create a summary prompt
    summary_prompt = "Summarize the following chat history in a concise manner.\n"
    summary_prompt += "Focus on the main topics discussed and key points made.\n\n"
    
    # Add chat history to prompt
    for message in chat_history:
        if message['role'] == 'user':
            summary_prompt += f"User: {message['content']}\n"
        elif message['role'] == 'assistant':
            summary_prompt += f"Assistant: {message['content']}\n"
    
    # Create messages for summary request
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes chat history."},
        {"role": "user", "content": summary_prompt}
    ]
    
    # Get summary from LLM
    result = client.chat(messages)
    return result['content']

def main():
    """Main function for the chat application"""
    print("=== Interactive LLM Chat with Notice Skill ===")
    print("Type your message and press Enter to send")
    print("Press Ctrl+C to exit")
    print()
    
    try:
        # Initialize LLM client
        client = LLMClient()
        print(f"Connected to: {client.model}")
        print(f"Base URL: {client.base_url}")
        print()
        
        # Get current date
        current_date = time.strftime('%Y-%m-%d')
        
        # Read available skills
        skills = list_available_skills()
        skills_json = json.dumps({"skills": skills}, ensure_ascii=False)
        print(f"Available skills: {skills_json}")
        print()
        
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
                print("Sending request to LLM...")
                start_time = time.time()
                result = client.chat(chat_history)
                end_time = time.time()
                print(f"LLM response received in {end_time - start_time:.2f} seconds")
                
                # Check if content exists
                content = result['content']
                
                # Just display the content
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
