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

## 技术栈

- **Python 3.14+**：核心编程语言
- **标准库**：urllib, json, time, os
- **本地LLM服务**：如LM Studio, Ollama等

## 注意事项

- 确保本地LLM服务正在运行
- 检查`.env`文件中的配置是否正确
- 本地LLM服务需要支持OpenAI兼容的API格式
- 对于不同的本地LLM服务，可能需要调整配置参数
