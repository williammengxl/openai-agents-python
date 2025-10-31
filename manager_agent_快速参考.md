# Manager Agent 快速参考

## ✅ 运行成功总结

刚刚成功运行了**语言翻译 Manager Agent**！

## 🎯 核心概念

### Manager 模式架构图

```
用户请求: "把 'Hello' 翻译成西班牙语、法语和意大利语"
    │
    ▼
┌─────────────────────────────────────────┐
│    翻译管理器 (Manager/Orchestrator)      │
│  ┌─────────────────────────────────┐   │
│  │ 分析: 需要3种语言翻译             │   │
│  │ 决策: 依次调用3个工具             │   │
│  └─────────────────────────────────┘   │
└─────┬───────────┬───────────┬───────────┘
      │           │           │
      │ 工具调用1  │ 工具调用2  │ 工具调用3
      │           │           │
┌─────▼─────┐ ┌──▼──────┐ ┌─▼──────────┐
│ Spanish   │ │ French  │ │ Italian    │
│ Translator│ │ Trans.  │ │ Translator │
│  Agent    │ │ Agent   │ │  Agent     │
└─────┬─────┘ └──┬──────┘ └─┬──────────┘
      │ 结果1     │ 结果2     │ 结果3
      └──────────┴───────────┴─────┐
                                   ▼
                        ┌─────────────────┐
                        │ 合成器 Agent     │
                        │ 整理所有翻译     │
                        └────────┬─────────┘
                                 ▼
                          最终格式化输出
```

## 📝 代码速查

### 1. 创建专业代理

```python
spanish_agent = Agent(
    name="西班牙语翻译专家",
    instructions="你是专业翻译，翻译成西班牙语",
)
```

### 2. 创建 Manager

```python
manager = Agent(
    name="翻译管理器",
    instructions="使用工具完成翻译，从不自己翻译",
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="翻译成西班牙语",
        ),
        # ... 更多工具
    ],
)
```

### 3. 运行

```python
result = await Runner.run(manager, "Translate 'Hello' to Spanish")
print(result.final_output)
```

## 🔥 快速运行

### 查看演示（无需 API Key）

```bash
cd /Users/williammeng/agent-ai/openai-agents-python/openai-agents-python
source .venv/bin/activate
python translation_manager_demo.py
```

**输出示例:**
```
✅ 已创建 4 个翻译工具
✅ 管理器代理: 翻译管理器
   - 工具数量: 4
   - 角色: 协调和调用专业翻译代理
📊 工作流程: [详细步骤]
💡 这是 'Manager模式' 的典型应用
```

### 运行实际翻译（需要 API Key）

```bash
export OPENAI_API_KEY='sk-your-key'
python translation_manager_demo.py
```

### 运行官方示例

```bash
# 查看官方代码
cat examples/agent_patterns/agents_as_tools.py

# 运行（需要 API Key）
python examples/agent_patterns/agents_as_tools.py
```

## 📊 关键对比

### Manager vs Handoffs

| | Manager 模式 | Handoffs 模式 |
|---|---|---|
| **API** | `.as_tool()` | `handoffs=[...]` |
| **控制** | Manager 控制 | 转移控制权 |
| **并发** | ✅ 可以 | ❌ 不可以 |
| **用途** | 协调多个专家 | 专门化分工 |

### 代码对比

```python
# Manager 模式 - 可以调用多个工具
manager = Agent(
    tools=[
        agent1.as_tool(),
        agent2.as_tool(),
        agent3.as_tool(),
    ]
)
# Manager 控制，可并行调用

# Handoffs 模式 - 转交控制权
triage = Agent(
    handoffs=[agent1, agent2, agent3]
)
# 选择一个并转移控制
```

## 🎯 使用场景

### ✅ 适合 Manager 模式

- 🌍 多语言翻译（同时翻译多种语言）
- 📊 金融分析（基本面分析 + 风险分析）
- 📝 研究报告（搜索 + 分析 + 写作）
- 🛍️ 电商助手（查询 + 推荐 + 比价）
- 📧 内容生成（写作 + 审核 + 格式化）

### ✅ 适合 Handoffs 模式

- 🗣️ 语言路由（识别语言并转接专家）
- 🎫 客服分流（问题分类并转接部门）
- 🏥 医疗咨询（症状判断并转接专科）

## 📁 文件位置

### 刚创建的演示文件

```
📄 translation_manager_demo.py         # 完整演示代码
📄 翻译Manager_Agent说明.md           # 详细文档
📄 manager_agent_快速参考.md          # 本文件
```

### 官方示例文件

```
📁 examples/agent_patterns/
  ├── agents_as_tools.py              # 基础 Manager 模式
  ├── agents_as_tools_conditional.py  # 条件工具启用
  ├── routing.py                      # Handoffs 对比
  └── README.md                       # 模式说明

📁 examples/
  ├── financial_research_agent/
  │   └── manager.py                  # 实战示例1
  └── research_bot/
      └── manager.py                  # 实战示例2

📁 docs/
  ├── tools.md                        # 英文文档
  └── zh/agents.md                    # 中文文档（第85行）
```

## 🚀 5分钟上手

### 步骤 1: 定义专家

```python
expert1 = Agent(name="专家1", instructions="...")
expert2 = Agent(name="专家2", instructions="...")
```

### 步骤 2: 创建 Manager

```python
manager = Agent(
    name="Manager",
    instructions="使用工具协调任务",
    tools=[
        expert1.as_tool(tool_name="task1", tool_description="..."),
        expert2.as_tool(tool_name="task2", tool_description="..."),
    ],
)
```

### 步骤 3: 运行

```python
result = await Runner.run(manager, "用户请求")
```

## 💡 关键提示

1. **Manager 的指令要明确说明"使用工具"**
   ```python
   "你从不自己翻译，而是始终使用提供的工具"
   ```

2. **工具描述要清晰**
   ```python
   tool_description="将用户的消息翻译成西班牙语"
   ```

3. **使用追踪查看整个流程**
   ```python
   with trace("My workflow"):
       result = await Runner.run(manager, input)
   ```

4. **可以添加合成器整理输出**
   ```python
   step1 = await Runner.run(manager, input)
   final = await Runner.run(synthesizer, step1.to_input_list())
   ```

## 📖 深入学习

### 阅读文档
```bash
# 中文文档
cat docs/zh/agents.md | less

# 英文文档
cat docs/tools.md | less
```

### 查看源码
```bash
# 查看 as_tool 实现
cat src/agents/agent.py | grep -A 30 "def as_tool"
```

### 运行测试
```bash
# 运行相关测试
pytest tests/test_agent_as_tool.py -v
```

## ❓ 常见问题

**Q: Manager 模式和 Handoffs 有什么区别？**  
A: Manager 保持控制权，可调用多个工具；Handoffs 转移控制权，只选一个。

**Q: 何时使用 Manager 模式？**  
A: 需要协调多个专家、并行处理、或保持中心控制时。

**Q: 可以动态启用/禁用工具吗？**  
A: 可以！使用 `is_enabled` 参数传递函数。

**Q: 如何追踪 Manager 的工具调用？**  
A: 使用 `with trace()` 包裹整个流程，在 OpenAI Dashboard 查看。

**Q: Manager 可以调用另一个 Manager 吗？**  
A: 可以！这样可以构建层次化的代理系统。

## 🎉 成功！

您已经成功：
- ✅ 理解了 Manager 模式概念
- ✅ 运行了语言翻译 Manager Agent
- ✅ 学会了如何创建和使用 Manager
- ✅ 掌握了与 Handoffs 模式的区别

## 下一步

1. 尝试添加更多语言支持
2. 实现条件工具启用
3. 构建自己的 Manager 应用
4. 查看金融研究示例了解实战应用

---

**快速命令**
```bash
# 运行演示
python translation_manager_demo.py

# 查看文档
cat 翻译Manager_Agent说明.md

# 运行官方示例
python examples/agent_patterns/agents_as_tools.py
```

