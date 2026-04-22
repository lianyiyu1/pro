# Chat with Summary

This is an interactive chat application with LLM integration, featuring chat history summarization, key information extraction, and chat history search functionality.

## Features

1. **Interactive Chat**: Communicate with an LLM model through a command-line interface
2. **Chat History Summarization**: Automatically summarizes chat history when it reaches a certain threshold
3. **Key Information Extraction**: Every 5 chat rounds, extracts key information using the 5W rule (Who, What, When, Where, Why) and saves it to `D:\chat-log\log.txt`
4. **Chat History Search**: Use the `/search` command or ask to "find chat history" to search through the saved key information
5. **Tool Integration**: Access various tools like file operations and web requests
6. **AnythingLLM Integration**: Query document repositories in AnythingLLM by mentioning "文档仓库", "文件仓库", or "仓库"

## How to Use

1. Ensure you have Python 3.7+ installed
2. Set up the `.env` file with your LLM configuration and AnythingLLM configuration
3. Run the script: `python chat_with_summary.py`
4. Type your messages and press Enter to send
5. Use `/search` followed by keywords to search chat history
6. Mention "文档仓库", "文件仓库", or "仓库" to query AnythingLLM document repositories
7. Press Ctrl+C to exit

## Key Information Extraction

The application automatically extracts key information every 5 chat rounds using the 5W rule:
- **Who**: Who is involved in the conversation
- **What**: What happened or was discussed
- **When**: When did it happen (optional)
- **Where**: Where did it happen (optional)
- **Why**: Why did it happen (optional)

Extracted information is saved to `D:\chat-log\log.txt` in an incremental manner.

## Chat History Search

To search chat history:
1. Type `/search` followed by your query
2. Or ask to "find chat history" with your query
3. The LLM will use the `search_chat_history` tool to retrieve relevant information

## Configuration

Create a `.env` file in the project root with the following variables:

```
LLM_BASE_URL=http://127.0.0.1:1234
LLM_MODEL=qwen/qwen3.5-9b
LLM_API_KEY=123456
LLM_TEMPERATURE=1
LLM_MAX_TOKENS=1000

# AnythingLLM Configuration
ANYTHINGLLM_API_KEY=your_anythingllm_api_key
ANYTHINGLLM_WORKSPACE_SLUG=your_workspace_slug
```

## Dependencies

- Python 3.7+
- Standard library modules: os, json, time, sys, urllib
- Custom tools from practice02

## Notes

- The application will create the `D:\chat-log` directory if it doesn't exist
- Key information is appended to `log.txt` in an incremental manner
- Chat history search uses the saved key information from `log.txt`
