# Practice06 - 链式工具调用 (Chained Tool Calls)

## 项目概述

本项目基于 practice05，实现了链式工具调用（Chained Tool Calls）功能，让 LLM 能够根据前一个工具的输出作为后一个工具的输入参数，自主决定下一步操作。

## 核心功能

### 1. ChainedCallContext 类
链式调用上下文管理器，用于在多个工具调用之间传递数据和状态：
- 记录每一步的调用和结果
- 存储中间变量供后续步骤使用
- 设置最大迭代次数，防止无限循环

### 2. execute_chained_tool_call 函数
实现链式工具调用的完整流程：
- 初始化消息历史，包含 system prompt
- 循环最多 max_iterations 次（默认10次）
- 构建分析提示词（包含用户请求和已执行的步骤历史）
- 调用 LLM 决定下一步操作
- 解析 LLM 响应（支持 JSON 格式和 tool_calls 格式）
- 如果任务完成，返回最终回答
- 如果需继续调用，执行工具并记录到上下文

### 3. build_analysis_prompt 函数
构建分析提示词，包含：
- 用户原始请求
- 已执行的工具调用历史（工具名、参数、结果）
- 决策规则说明
- JSON 输出格式要求

### 4. extract_json_from_response 函数
从 LLM 响应中提取 JSON，处理 markdown 代码块标记

## 支持的工具

| 工具名称 | 功能描述 | 参数 |
|---------|---------|------|
| `list_files` | 列出目录下的文件 | `directory`: 目录路径 |
| `search_files` | 搜索包含指定模式的文件 | `directory`: 目录路径, `pattern`: 搜索模式 |
| `read_file` | 读取文件内容 | `filepath`: 文件路径 |
| `load_skill_content` | 加载技能内容 | `skill_name`: 技能名称 |
| `curl` | 获取网页内容 | `url`: 网页地址, `timeout`: 超时时间 |
| `create_file` | 创建文件 | `directory`: 目录路径, `filename`: 文件名, `content`: 文件内容 |

## 输出格式

LLM 需要按照以下 JSON 格式返回决策：

### 完成任务时
```json
{"done": true, "answer": "最终回答内容"}
```

### 继续调用工具时
```json
{"done": false, "tool_call": {"name": "工具名称", "arguments": {"参数名": "参数值"}}}
```

## 链式调用规则

1. 可以将前一个工具的输出作为后一个工具的输入参数
2. 根据中间结果自主决定下一步操作
3. 可以使用上下文变量存储和传递中间结果
4. 当获得足够信息时，总结并回答用户
5. 支持工具调用的顺序依赖关系
6. 最多执行 10 次工具调用，避免无限循环

## 使用方法

### 交互式模式
```bash
python chat_with_chained_calls.py
```

### 编程方式调用
```python
from chat_with_chained_calls import LLMClient, execute_chained_tool_call

client = LLMClient()
result = execute_chained_tool_call(client, "请查找 practice05 目录下所有包含'def'关键词的文件", max_iterations=10)
print(result)
```

## 测试用例

### 测试1：文件搜索链式调用
```
用户请求："请查找 practice05 目录下所有包含'def'关键词的文件，并总结这些文件的主要内容"
执行流程：search_files → read_file → 总结回答
```

### 测试2：技能查询链式调用
```
用户请求："我想了解 notice 技能的详细规则"
执行流程：load_skill_content → 总结回答
```

### 测试3：网页处理链式调用
```
用户请求："访问 https://www.nsu.edu.cn/HTML/news/2024/06/article_3974.html 并总结页面内容，保存到 practice06/summary.txt"
执行流程：curl → create_file → 总结回答
```

## 运行测试

```bash
python test_chained_calls.py
```

## 项目结构

```
practice06/
├── chat_with_chained_calls.py    # 主程序文件
├── test_chained_calls.py         # 测试脚本
└── README.md                     # 项目文档
```

## 注意事项

1. **JSON 解析**：LLM 可能返回包含 markdown 代码块标记（如 \`\`\`json）的内容，需要先提取 JSON 部分再解析
2. **响应格式**：LLM 可能返回 tool_calls 格式（OpenAI 标准 Function Calling 格式）或 JSON content 格式，需要同时支持
3. **错误处理**：检查 LLM 响应是否为 None，处理 JSON 解析失败的情况，处理工具执行异常
4. **防止无限循环**：设置 max_iterations 限制最大迭代次数（默认 10 次）