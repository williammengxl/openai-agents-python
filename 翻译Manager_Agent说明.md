# 语言翻译 Manager Agent 说明

## 🎉 运行成功！

刚刚成功运行了语言翻译的 Manager Agent 演示。

## 📋 什么是 Manager 模式？

**Manager 模式**（也叫 **Orchestrator 模式** 或 **Agents as Tools 模式**）是一种常用的多代理架构模式：

```
                  ┌─────────────────────┐
                  │   Manager Agent     │
                  │   (Orchestrator)    │
                  └──────────┬──────────┘
                             │
                 ┌───────────┼───────────┐
                 │           │           │
          ┌──────▼─────┐ ┌──▼─────┐ ┌──▼──────┐
          │ Spanish    │ │ French │ │ Italian │
          │ Translator │ │ Trans. │ │ Trans.  │
          │  (Tool)    │ │ (Tool) │ │ (Tool)  │
          └────────────┘ └────────┘ └─────────┘
```

### 核心特点

1. **中心化控制** - Manager 代理始终控制对话流程
2. **工具调用** - 专业代理作为工具被调用
3. **协调能力** - Manager 决定何时调用哪个工具
4. **可组合** - 可以调用多个工具完成复杂任务

## 🏗️ 架构组件

### 1. 专业翻译代理（作为工具）

```python
spanish_agent = Agent(
    name="西班牙语翻译专家",
    instructions="你是专业的英语到西班牙语翻译，准确地翻译用户的消息到西班牙语。",
    handoff_description="英语到西班牙语的专业翻译",
)

french_agent = Agent(
    name="法语翻译专家",
    instructions="你是专业的英语到法语翻译，准确地翻译用户的消息到法语。",
)

# ... 更多翻译代理
```

### 2. 管理器/编排器代理

```python
orchestrator_agent = Agent(
    name="翻译管理器",
    instructions=(
        "你是一个翻译管理器。你使用提供的工具来完成翻译任务。"
        "如果用户要求多种语言的翻译，你要按顺序调用相关的工具。"
        "你从不自己翻译，而是始终使用提供的工具来完成翻译。"
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="将用户的消息翻译成西班牙语",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="将用户的消息翻译成法语",
        ),
        # ... 更多工具
    ],
)
```

### 3. 合成器代理（可选）

```python
synthesizer_agent = Agent(
    name="翻译合成器",
    instructions=(
        "你检查各种语言的翻译，必要时进行修正，"
        "并产生一个最终的、格式良好的综合响应。"
    ),
)
```

## 🔄 工作流程

1. **用户请求** → "Translate 'Hello' to Spanish, French, and Italian"
2. **Manager 分析** → 识别需要3种语言翻译
3. **工具调用 1** → 调用 `translate_to_spanish` 工具
4. **Spanish Agent** → 返回西班牙语翻译
5. **工具调用 2** → 调用 `translate_to_french` 工具
6. **French Agent** → 返回法语翻译
7. **工具调用 3** → 调用 `translate_to_italian` 工具
8. **Italian Agent** → 返回意大利语翻译
9. **合成器处理** → 整理所有翻译
10. **最终输出** → 格式化的多语言翻译结果

## 🎯 使用方法

### 运行演示（架构说明）

```bash
cd /Users/williammeng/agent-ai/openai-agents-python/openai-agents-python
source .venv/bin/activate
python translation_manager_demo.py
```

### 运行实际翻译（需要 API Key）

```bash
# 设置 API Key
export OPENAI_API_KEY='sk-your-api-key-here'

# 运行演示
python translation_manager_demo.py
```

### 运行官方示例

```bash
# 基础的 agents-as-tools 模式
python examples/agent_patterns/agents_as_tools.py

# 带条件工具启用的版本
python examples/agent_patterns/agents_as_tools_conditional.py
```

## 📊 与其他模式的对比

### Manager 模式 vs Handoffs 模式

| 特性 | Manager 模式 | Handoffs 模式 |
|------|-------------|---------------|
| **控制权** | Manager 始终控制 | 控制权转移给新代理 |
| **对话历史** | Manager 看到全部历史 | 新代理接管历史 |
| **适用场景** | 需要协调多个专家 | 专门化任务分工 |
| **示例** | 翻译多种语言 | 语言路由 |
| **代码** | `agent.as_tool()` | `handoffs=[agent]` |

### 示例对比

**Manager 模式:**
```python
# Manager 调用多个翻译工具
orchestrator = Agent(
    tools=[
        spanish_agent.as_tool(...),
        french_agent.as_tool(...),
    ]
)
# Manager 保持控制，可以并行调用多个工具
```

**Handoffs 模式:**
```python
# Triage 转交给专家
triage_agent = Agent(
    handoffs=[spanish_agent, french_agent]
)
# 控制权完全转移，只能选一个
```

## 🔧 高级功能

### 1. 条件工具启用

```python
from agents import RunContextWrapper

def premium_only(ctx: RunContextWrapper[Context], agent) -> bool:
    return ctx.context.user_tier == "premium"

orchestrator = Agent(
    tools=[
        basic_tool.as_tool(is_enabled=True),
        premium_tool.as_tool(is_enabled=premium_only),
    ]
)
```

### 2. 自定义输出提取器

```python
async def extract_summary(result) -> str:
    return result.final_output.summary

agent.as_tool(
    custom_output_extractor=extract_summary
)
```

### 3. 追踪整个编排

```python
with trace("Translation Orchestration"):
    result = await Runner.run(orchestrator_agent, text)
    # 所有工具调用都在同一个追踪中
```

## 📚 实际应用场景

### 1. 多语言翻译服务
- ✅ Manager: 翻译协调器
- ✅ Tools: 各语言翻译专家

### 2. 金融研究分析
```python
writer_agent = Agent(
    tools=[
        fundamentals_agent.as_tool(),
        risk_agent.as_tool(),
    ]
)
```

### 3. 客户服务系统
```python
customer_agent = Agent(
    tools=[
        booking_agent.as_tool(),
        refund_agent.as_tool(),
        support_agent.as_tool(),
    ]
)
```

### 4. 研究助手
```python
research_manager = Agent(
    tools=[
        planner_agent.as_tool(),
        search_agent.as_tool(),
        writer_agent.as_tool(),
    ]
)
```

## 💡 最佳实践

### 1. 清晰的工具描述
```python
spanish_agent.as_tool(
    tool_name="translate_to_spanish",  # 简洁的名称
    tool_description="将用户的消息翻译成西班牙语",  # 清晰的描述
)
```

### 2. Manager 的指令要明确
```python
instructions=(
    "你是一个翻译管理器。"
    "你从不自己翻译，而是始终使用提供的工具。"  # 关键！
    "如果要求多种语言，按顺序调用工具。"
)
```

### 3. 使用合成器整理输出
```python
# 步骤1: Manager 协调工具调用
orchestrator_result = await Runner.run(orchestrator_agent, input)

# 步骤2: 合成器整理输出
final_result = await Runner.run(
    synthesizer_agent, 
    orchestrator_result.to_input_list()
)
```

### 4. 统一追踪
```python
with trace("Complete workflow"):
    # 所有操作在一个追踪中
    pass
```

## 🎓 学习资源

### 官方文档
- **英文**: `docs/tools.md` - Agents as Tools 部分
- **中文**: `docs/zh/agents.md` - 第85行开始

### 示例代码
1. **基础示例**: `examples/agent_patterns/agents_as_tools.py`
2. **条件工具**: `examples/agent_patterns/agents_as_tools_conditional.py`
3. **金融研究**: `examples/financial_research_agent/manager.py`
4. **研究机器人**: `examples/research_bot/manager.py`

### 架构指南
- **OpenAI 实用指南**: [Building Agents Guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

## 🚀 下一步

1. **运行官方示例**
   ```bash
   python examples/agent_patterns/agents_as_tools.py
   ```

2. **查看中文文档**
   ```bash
   cat docs/zh/agents.md | grep -A 30 "管理器"
   ```

3. **尝试修改代码**
   - 添加更多语言（德语、日语等）
   - 实现条件工具启用
   - 添加自定义输出格式

4. **构建自己的Manager**
   - 选择你的应用场景
   - 定义专业代理
   - 创建Manager协调器
   - 测试和优化

---

**状态**: ✅ 演示运行成功  
**文件**: `translation_manager_demo.py`  
**模式**: Manager (Agents as Tools)  
**版本**: openai-agents 0.4.2

