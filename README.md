# AI智能体开发教学项目

## 项目简介

本项目是一个基于Python的AI智能体开发教学项目，旨在帮助学习者掌握：
- Python标准库的使用
- API调用与响应处理
- 环境配置管理
- 性能统计与分析
- OpenAI兼容LLM的使用

## 项目结构

```
pro/
├── practice01/           # 练习1：LLM客户端实现
│   └── llm_client.py     # Python标准库实现的LLM客户端
├── practice02/           # 练习2：工具调用功能
│   ├── tools.py          # 工具函数模块
│   └── chat_with_tools.py # 带工具调用的聊天界面
├── venv/                 # Python虚拟环境
├── .env                  # 环境配置文件
├── .env.example          # 环境配置模板
├── env.example           # 环境配置模板（备用）
├── .gitignore            # Git忽略文件
├── requirements.txt      # 项目依赖
└── README.md             # 项目说明文档
```

## 练习1：LLM客户端实现

### 文件：`practice01/llm_client.py`

#### 功能用途
1. **配置管理**：读取项目根目录的`.env`文件，加载LLM配置
2. **API调用**：使用Python标准库`urllib`发送HTTP请求到OpenAI兼容的LLM服务
3. **错误处理**：处理HTTP错误、URL错误、JSON解析错误等异常情况
4. **响应解析**：解析LLM返回的JSON响应
5. **性能统计**：计算请求耗时、token消耗、生成速度等指标
6. **结果展示**：显示LLM响应内容和详细的统计信息

#### 教学目标

1. **Python标准库应用**
   - 学习使用`urllib`模块进行HTTP请求
   - 学习使用`json`模块处理JSON数据
   - 学习使用`time`模块进行时间统计
   - 学习使用`os`模块进行文件操作

2. **API集成技能**
   - 理解OpenAI兼容API的请求格式
   - 掌握HTTP请求的构建和发送
   - 学习处理API响应和错误

3. **环境配置管理**
   - 学习使用`.env`文件管理配置
   - 理解配置文件的读取和解析
   - 掌握默认值和错误处理

4. **性能分析能力**
   - 学习如何统计API调用性能
   - 理解token消耗的计算方法
   - 掌握速度分析的基本方法

5. **错误处理实践**
   - 学习异常捕获和处理
   - 掌握错误信息的格式化和展示
   - 理解不同类型错误的处理策略

## 快速开始

### 1. 配置环境

复制环境配置模板并填写正确的配置：

```bash
copy env.example .env
```

编辑`.env`文件：

```
# OpenAI Compatible LLM Configuration
LLM_BASE_URL=http://127.0.0.1:1234  # 本地LLM服务地址
LLM_MODEL=qwen/qwen3.5-9b             # 模型名称
LLM_API_KEY=123456                    # API密钥（本地服务通常不需要真实密钥）
LLM_TEMPERATURE=1.0                    # 温度参数
LLM_MAX_TOKENS=1000                   # 最大token数
```

### 2. 激活虚拟环境

**Windows PowerShell**：
```powershell
.envcriptsctivate.ps1
```

**Windows CMD**：
```cmd
venvcriptsctivate.bat
```

### 3. 运行示例

```bash
python practice01\llm_client.py
```

## 预期输出

```
=== LLM Client Demo ===

Sending request to LLM...
Model: qwen/qwen3.5-9b
Base URL: http://127.0.0.1:1234/v1

=== API Response ===
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1712889600,
  "model": "qwen/qwen3.5-9b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "我是一个基于Qwen3.5-9B模型的AI助手，能够回答各种问题，提供信息和帮助。"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 25,
    "total_tokens": 35
  }
}
====================

=== Response ===
Content:
我是一个基于Qwen3.5-9B模型的AI助手，能够回答各种问题，提供信息和帮助。

=== Usage Statistics ===
Elapsed Time: 1.23 seconds
Prompt Tokens: 10
Completion Tokens: 25
Total Tokens: 35
Tokens per Second: 20.33
```

## 学习要点

1. **HTTP请求构建**：了解如何使用`urllib.Request`构建POST请求
2. **JSON数据处理**：学习如何序列化请求数据和解析响应数据
3. **错误处理机制**：掌握try-except结构处理各种异常
4. **性能统计方法**：学习如何使用时间戳和响应数据计算性能指标
5. **配置管理**：理解环境变量的加载和使用

## 扩展练习

1. **添加更多模型支持**：修改代码支持不同的LLM模型
2. **实现流式响应**：添加流式响应处理功能
3. **添加重试机制**：实现请求失败时的自动重试
4. **支持更多API参数**：添加对top_p、frequency_penalty等参数的支持
5. **实现缓存机制**：缓存重复请求的响应

## 练习2：交互式聊天界面

### 文件：`practice02/chat_interface.py`

#### 功能用途
1. **终端交互**：支持在终端中输入聊天内容
2. **流式输出**：实时显示LLM的响应内容
3. **历史记录**：自动将聊天历史添加到上下文
4. **持续对话**：循环运行直到用户按下Ctrl+C退出
5. **错误处理**：处理各种异常情况并提供友好的错误信息
6. **性能统计**：显示每次请求的耗时、token消耗和生成速度

#### 教学目标

1. **交互式应用开发**
   - 学习如何构建命令行交互式应用
   - 掌握用户输入的获取和处理
   - 学习如何实现循环对话逻辑

2. **流式响应处理**
   - 理解SSE (Server-Sent Events) 格式
   - 学习如何处理流式API响应
   - 掌握实时输出的实现方法

3. **上下文管理**
   - 学习如何维护对话历史
   - 理解上下文在LLM对话中的重要性
   - 掌握如何将历史记录添加到请求中

4. **异常处理**
   - 学习如何处理键盘中断（Ctrl+C）
   - 掌握异常捕获和恢复机制
   - 理解错误处理对用户体验的影响

5. **用户体验优化**
   - 学习如何实现友好的终端界面
   - 掌握实时反馈的实现方法
   - 理解如何提供清晰的用户提示

### 运行方法

```bash
python practice02\chat_interface.py
```

### 预期交互

```
=== Interactive LLM Chat ===
Type your message and press Enter to send
Press Ctrl+C to exit

Connected to: qwen/qwen3.5-9b
Base URL: http://127.0.0.1:1234/v1

You: Hello!
AI: Hello! How can I help you today?

[Stats] Time: 1.23s, Tokens: 35, Speed: 20.33 tokens/s
==================================================
You: What's the capital of France?
AI: The capital of France is Paris.

[Stats] Time: 0.87s, Tokens: 28, Speed: 25.29 tokens/s
==================================================
You: Ctrl+C
Exiting chat...
```

## 技术栈

- **Python 3.14+**：核心编程语言
- **标准库**：urllib, json, time, os, sys
- **本地LLM服务**：如LM Studio, Ollama等

## 注意事项

- 确保本地LLM服务正在运行
- 检查`.env`文件中的配置是否正确
- 本地LLM服务需要支持OpenAI兼容的API格式和流式响应
- 对于不同的本地LLM服务，可能需要调整配置参数
- 长时间对话可能会累积较多的上下文，导致token消耗增加

## 练习2：工具调用功能

### 文件：`practice02/tools.py`

#### 功能用途
1. **list_files**：列出目录下的文件及其属性（大小、修改时间等）
2. **rename_file**：修改目录下文件的名称
3. **delete_file**：删除目录下的文件
4. **create_file**：在目录下创建新文件并写入内容
5. **read_file**：读取目录下文件的内容

### 文件：`practice02/chat_with_tools.py`

#### 功能用途
1. **工具调用**：支持LLM通过JSON格式调用工具函数
2. **系统提示**：包含工具函数的详细说明和使用格式
3. **工具执行**：执行LLM请求的工具操作
4. **结果处理**：将工具执行结果返回给LLM
5. **交互式聊天**：支持持续对话，直到用户按下Ctrl+C退出

#### 教学目标

1. **工具集成能力**
   - 学习如何将外部工具集成到LLM系统中
   - 掌握工具调用的设计模式
   - 理解工具参数的传递和处理

2. **系统提示工程**
   - 学习如何编写有效的系统提示词
   - 掌握工具使用说明的编写方法
   - 理解系统提示对LLM行为的影响

3. **JSON解析与处理**
   - 学习如何解析LLM返回的JSON格式工具调用
   - 掌握JSON数据的验证和错误处理

4. **多轮对话管理**
   - 学习如何管理包含工具调用的多轮对话
   - 理解工具执行结果在对话中的作用

5. **错误处理与恢复**
   - 学习如何处理工具执行错误
   - 掌握错误信息的传递和展示

### 运行方法

```bash
python practice02\chat_with_tools.py
```

### 预期交互

```
=== Interactive LLM Chat with Tool Calling ===
Type your message and press Enter to send
Press Ctrl+C to exit

Connected to: qwen/qwen3.5-9b
Base URL: http://127.0.0.1:1234/v1

You: 列出practice02目录下的文件
AI: {
  "tool_call": {
    "name": "list_files",
    "arguments": {
      "directory": "practice02"
    }
  }
}

Executing tool: list_files
Arguments: {
  "directory": "practice02"
}
Tool execution result: {
  "success": true,
  "directory": "practice02",
  "file_count": 2,
  "files": [
    {
      "name": "tools.py",
      "path": "practice02\\tools.py",
      "is_directory": false,
      "size": 4096,
      "last_modified": "2026-04-13 16:17:00"
    },
    {
      "name": "chat_with_tools.py",
      "path": "practice02\\chat_with_tools.py",
      "is_directory": false,
      "size": 8192,
      "last_modified": "2026-04-13 16:18:00"
    }
  ]
}

AI: practice02目录下有2个文件：
1. tools.py - 大小：4096字节，最后修改时间：2026-04-13 16:17:00
2. chat_with_tools.py - 大小：8192字节，最后修改时间：2026-04-13 16:18:00

[Stats] Time: 2.34s, Tokens: 150, Speed: 45.67 tokens/s
==================================================
You: 在practice02目录下创建一个test.txt文件，内容为"Hello, Tool Calling!"
AI: {
  "tool_call": {
    "name": "create_file",
    "arguments": {
      "directory": "practice02",
      "filename": "test.txt",
      "content": "Hello, Tool Calling!"
    }
  }
}

Executing tool: create_file
Arguments: {
  "directory": "practice02",
  "filename": "test.txt",
  "content": "Hello, Tool Calling!"
}
Tool execution result: {
  "success": true,
  "file_path": "practice02\\test.txt",
  "content_length": 19
}

AI: 文件已成功创建，路径为：practice02\\test.txt，内容长度为19个字符。

[Stats] Time: 1.87s, Tokens: 120, Speed: 50.26 tokens/s
==================================================
You: 读取practice02目录下的test.txt文件内容
AI: {
  "tool_call": {
    "name": "read_file",
    "arguments": {
      "directory": "practice02",
      "filename": "test.txt"
    }
  }
}

Executing tool: read_file
Arguments: {
  "directory": "practice02",
  "filename": "test.txt"
}
Tool execution result: {
  "success": true,
  "file_path": "practice02\\test.txt",
  "size": 19,
  "content": "Hello, Tool Calling!"
}

AI: 文件内容为：Hello, Tool Calling!

[Stats] Time: 1.56s, Tokens: 100, Speed: 55.12 tokens/s
==================================================
```

### 工具调用格式

LLM需要使用以下JSON格式来调用工具：

```json
{
  "tool_call": {
    "name": "tool_name",
    "arguments": {
      "parameter1": "value1",
      "parameter2": "value2"
    }
  }
}
```

### 工具调用示例

**访问网页示例**：
```json
{
  "tool_call": {
    "name": "curl",
    "arguments": {
      "url": "https://www.example.com",
      "timeout": 10
    }
  }
}
```

### 可用工具列表

1. **list_files(directory: str)**
   - 列出目录下的所有文件及其属性
   - 参数：directory（目录路径）

2. **rename_file(directory: str, old_name: str, new_name: str)**
   - 修改文件名称
   - 参数：directory（目录路径）、old_name（旧文件名）、new_name（新文件名）

3. **delete_file(directory: str, filename: str)**
   - 删除指定文件
   - 参数：directory（目录路径）、filename（文件名）

4. **create_file(directory: str, filename: str, content: str)**
   - 创建新文件并写入内容
   - 参数：directory（目录路径）、filename（文件名）、content（文件内容）

5. **read_file(directory: str, filename: str)**
   - 读取文件内容
   - 参数：directory（目录路径）、filename（文件名）

6. **curl(url: str, timeout: int = 30)**
   - 通过curl访问网页并返回网页内容
   - 参数：url（网页URL）、timeout（超时时间，默认30秒）

## 练习3：聊天记录总结功能

### 文件：`practice03/chat_with_summary.py`

#### 功能用途
1. **聊天历史检测**：检测聊天历史记录，当超过5轮或上下文长度超过3k时触发总结
2. **自动总结**：调用LLM对聊天记录进行自动总结
3. **聊天记录压缩**：对前70%左右的内容进行压缩，最后30%左右的内容保留原文
4. **工具调用**：保留了practice02中的工具调用功能
5. **交互式聊天**：支持持续对话，直到用户按下Ctrl+C退出

#### 教学目标

1. **聊天历史管理**
   - 学习如何检测聊天历史的长度和轮数
   - 掌握聊天记录压缩的实现方法
   - 理解上下文管理对LLM性能的影响

2. **自动总结功能**
   - 学习如何使用LLM生成聊天记录总结
   - 掌握总结提示词的编写技巧
   - 理解总结对减少token消耗的作用

3. **性能优化**
   - 学习如何通过总结减少上下文长度
   - 掌握token消耗的优化方法
   - 理解长对话的处理策略

4. **代码结构设计**
   - 学习如何在现有代码基础上添加新功能
   - 掌握模块化代码的设计方法
   - 理解代码的可维护性和可扩展性

### 运行方法

```bash
python practice03\chat_with_summary.py
```

### 预期交互

```
=== Interactive LLM Chat with Tool Calling and History Summary ===
Type your message and press Enter to send
Press Ctrl+C to exit

Connected to: qwen/qwen3.5-9b
Base URL: http://127.0.0.1:1234/v1

You: Hello!
AI: Hello! How can I help you today?

[Stats] Time: 1.23s, Tokens: 35, Speed: 20.33 tokens/s
======================================================================
You: What's the capital of France?
AI: The capital of France is Paris.

[Stats] Time: 0.87s, Tokens: 28, Speed: 25.29 tokens/s
======================================================================
... (after 5 rounds or context over 3k)

=== Chat history threshold reached, generating summary ===
Current conversation rounds: 5
Current context length: 3200

=== Generating chat summary ===
=== API Response ===
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1712889600,
  "model": "qwen/qwen3.5-9b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The user greeted me and asked about the capital of France. I responded that Paris is the capital of France."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 30,
    "total_tokens": 130
  }
}
====================
=== Summary generated ===
The user greeted me and asked about the capital of France. I responded that Paris is the capital of France.

=== Chat history compressed ===
New context length: 500
New message count: 3

You: What's the population of Paris?
AI: The population of Paris is approximately 2.1 million people within the city limits, and around 12 million people in the greater Paris metropolitan area.

[Stats] Time: 1.56s, Tokens: 45, Speed: 22.50 tokens/s
======================================================================
```

### 总结功能说明

1. **触发条件**：
   - 聊天轮数超过5轮
   - 聊天上下文长度超过3000字符

2. **压缩策略**：
   - 对前70%的聊天内容生成总结
   - 保留最后30%的聊天内容原文
   - 系统消息始终保留

3. **总结过程**：
   - 提取用户和助手的对话内容
   - 调用LLM生成简洁的总结
   - 将总结替换为一条消息
   - 更新聊天历史为压缩版本

## 练习4：关键信息提取与聊天历史查找

### 文件：`practice03/chat_with_keyinfo.py`

#### 功能用途
1. **关键信息提取**：每五次聊天提取一次关键信息，按照5W规则（谁Who、做了什么事What、什么时候When、在何处Where、为什么要做这个事Why）进行提取
2. **本地记录**：将提取的关键信息记录到本地电脑D:\chat-log\log.txt文件中，支持增量更新
3. **聊天历史查找**：实现了search_chat_history工具，当用户发送的信息用"/search"开头，或表达了"查找聊天历史"的意思时，可查找聊天历史记录
4. **工具调用**：保留了之前的工具调用功能
5. **聊天记录压缩**：保留了聊天记录压缩功能

#### 教学目标

1. **关键信息提取**
   - 学习如何使用LLM提取关键信息
   - 掌握5W规则的应用方法
   - 理解信息提取对对话分析的重要性

2. **本地文件操作**
   - 学习如何创建目录和文件
   - 掌握文件的增量更新方法
   - 理解本地存储对聊天历史管理的作用

3. **聊天历史查找**
   - 学习如何实现聊天历史的检索功能
   - 掌握工具调用的设计和实现
   - 理解用户意图识别的基本方法

4. **多功能集成**
   - 学习如何在现有代码基础上集成多种功能
   - 掌握模块化代码的设计方法
   - 理解功能之间的交互和协调

### 运行方法

```bash
python practice03\chat_with_keyinfo.py
```

### 预期交互

```
=== Interactive LLM Chat with Tool Calling, Summary, and Key Info Extraction ===
Type your message and press Enter to send
Press Ctrl+C to exit

Connected to: qwen/qwen3.5-9b
Base URL: http://127.0.0.1:1234/v1

You: Hello!
AI: Hello! How can I help you today?

[Stats] Time: 1.23s, Tokens: 35, Speed: 20.33 tokens/s
======================================================================
... (after 5 rounds)

=== Extracting key information from chat history ===

=== API Response ===
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1712889600,
  "model": "qwen/qwen3.5-9b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "1. Who: User and AI assistant\nWhat: Greeted each other and started conversation\n\n2. Who: User\nWhat: Asked about the capital of France\n\n3. Who: AI assistant\nWhat: Answered that Paris is the capital of France"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 200,
    "completion_tokens": 50,
    "total_tokens": 250
  }
}
====================
=== Key information extracted ===
1. Who: User and AI assistant
What: Greeted each other and started conversation

2. Who: User
What: Asked about the capital of France

3. Who: AI assistant
What: Answered that Paris is the capital of France

Key information saved to D:\chat-log\log.txt
=== Key information extraction completed ===

You: /search capital of France
AI: {
  "tool_call": {
    "name": "search_chat_history",
    "arguments": {
      "query": "capital of France"
    }
  }
}

Executing tool: search_chat_history
Arguments: {
  "query": "capital of France"
}
Tool execution result: {
  "success": true,
  "log_content": "=== 2026-04-15 12:00:00 ===\n1. Who: User and AI assistant\nWhat: Greeted each other and started conversation\n\n2. Who: User\nWhat: Asked about the capital of France\n\n3. Who: AI assistant\nWhat: Answered that Paris is the capital of France\n",
  "query": "capital of France"
}

AI: I found information about the capital of France in your chat history. You asked about the capital of France, and I answered that Paris is the capital of France.

[Stats] Time: 1.56s, Tokens: 80, Speed: 25.00 tokens/s
======================================================================
```

### 功能说明

1. **关键信息提取**：
   - 每五次聊天自动触发
   - 按照5W规则提取信息
   - 支持多条关键信息提取
   - 自动保存到本地文件

2. **聊天历史查找**：
   - 支持以"/search"开头的查询
   - 支持表达"查找聊天历史"意图的查询
   - 可根据查询内容搜索历史记录
   - 将搜索结果与用户请求结合，提供完整回复

3. **本地存储**：
   - 自动创建目录和文件
   - 支持增量更新
   - 记录时间戳和关键信息
   - 便于后续查询和分析
