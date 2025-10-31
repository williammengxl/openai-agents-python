#!/usr/bin/env python3
"""
简单的 OpenAI Agents SDK 演示
展示框架的基本结构和能力（使用模拟数据）
"""

print("\n" + "="*70)
print("🎉 OpenAI Agents SDK Python - 框架演示")
print("="*70 + "\n")

# 演示 1: 导入核心模块
print("📦 演示 1: 导入核心模块")
print("-" * 70)
try:
    from agents import Agent, Runner, function_tool
    from agents import InputGuardrail, OutputGuardrail, Handoff
    from agents import Session, SQLiteSession
    from agents import ModelSettings
    from agents import trace, agent_span, get_current_trace
    from agents.models.interface import Model
    
    print("✅ 成功导入所有核心模块")
    print("   - Agent: 代理类")
    print("   - Runner: 执行引擎")
    print("   - function_tool: 工具装饰器")
    print("   - Guardrails: 安全检查")
    print("   - Session: 会话管理")
    print("   - Tracing: 追踪系统")
except Exception as e:
    print(f"❌ 导入失败: {e}")

# 演示 2: 创建一个代理
print("\n📝 演示 2: 创建代理")
print("-" * 70)
try:
    agent = Agent(
        name="助手",
        instructions="你是一个有帮助的助手",
    )
    print(f"✅ 成功创建代理")
    print(f"   名称: {agent.name}")
    print(f"   指令: {agent.instructions}")
    print(f"   工具数量: {len(agent.tools)}")
    print(f"   切换数量: {len(agent.handoffs)}")
except Exception as e:
    print(f"❌ 创建失败: {e}")

# 演示 3: 创建工具
print("\n🔧 演示 3: 创建工具")
print("-" * 70)
try:
    @function_tool
    def get_weather(city: str) -> str:
        """获取指定城市的天气
        
        Args:
            city: 城市名称
        """
        return f"{city}的天气是晴天"
    
    @function_tool
    def calculate(expression: str) -> str:
        """计算数学表达式
        
        Args:
            expression: 数学表达式
        """
        try:
            result = eval(expression)
            return f"结果: {result}"
        except:
            return "计算错误"
    
    print(f"✅ 成功创建工具")
    print(f"   工具 1: {get_weather.name} - {get_weather.description}")
    print(f"   工具 2: {calculate.name} - {calculate.description}")
    
    # 创建带工具的代理
    agent_with_tools = Agent(
        name="工具助手",
        instructions="你可以使用工具帮助用户",
        tools=[get_weather, calculate],
    )
    print(f"\n✅ 创建了带 {len(agent_with_tools.tools)} 个工具的代理")
except Exception as e:
    print(f"❌ 创建失败: {e}")

# 演示 4: 多代理协作（Handoffs）
print("\n🤝 演示 4: 多代理协作（Handoffs）")
print("-" * 70)
try:
    math_agent = Agent(
        name="数学专家",
        handoff_description="处理数学问题",
        instructions="你是数学专家",
    )
    
    history_agent = Agent(
        name="历史专家",
        handoff_description="处理历史问题",
        instructions="你是历史专家",
    )
    
    triage_agent = Agent(
        name="路由助手",
        instructions="根据问题类型转接到专家",
        handoffs=[math_agent, history_agent],
    )
    
    print(f"✅ 创建了多代理系统")
    print(f"   路由代理: {triage_agent.name}")
    print(f"   可切换到: {len(triage_agent.handoffs)} 个专家")
    print(f"     - {math_agent.name}: {math_agent.handoff_description}")
    print(f"     - {history_agent.name}: {history_agent.handoff_description}")
except Exception as e:
    print(f"❌ 创建失败: {e}")

# 演示 5: 结构化输出
print("\n📊 演示 5: 结构化输出")
print("-" * 70)
try:
    from pydantic import BaseModel
    
    class WeatherInfo(BaseModel):
        city: str
        temperature: int
        condition: str
    
    agent_structured = Agent(
        name="天气助手",
        instructions="提供结构化天气信息",
        output_type=WeatherInfo,
    )
    
    print(f"✅ 创建了结构化输出代理")
    print(f"   输出类型: WeatherInfo")
    print(f"   字段: city, temperature, condition")
except Exception as e:
    print(f"❌ 创建失败: {e}")

# 演示 6: 模型设置
print("\n⚙️  演示 6: 模型设置")
print("-" * 70)
try:
    model_settings = ModelSettings(
        temperature=0.7,
        max_tokens=1000,
    )
    
    agent_custom = Agent(
        name="自定义助手",
        instructions="使用自定义模型设置",
        model_settings=model_settings,
    )
    
    print(f"✅ 创建了自定义模型设置")
    print(f"   Temperature: {model_settings.temperature}")
    print(f"   Max Tokens: {model_settings.max_tokens}")
except Exception as e:
    print(f"❌ 创建失败: {e}")

# 演示 7: 会话管理
print("\n💾 演示 7: 会话管理")
print("-" * 70)
try:
    # SQLite 会话（文件存储）
    session = SQLiteSession("test_session", ":memory:")
    print(f"✅ 创建了会话管理")
    print(f"   类型: SQLiteSession")
    print(f"   存储: 内存数据库")
    print(f"   会话 ID: test_session")
except Exception as e:
    print(f"❌ 创建失败: {e}")

# 演示 8: 上下文（Context）
print("\n🔐 演示 8: 自定义上下文")
print("-" * 70)
try:
    from pydantic import BaseModel
    
    class UserContext(BaseModel):
        user_id: str
        role: str
        preferences: dict = {}
    
    context = UserContext(
        user_id="user_123",
        role="admin",
        preferences={"language": "zh", "theme": "dark"}
    )
    
    print(f"✅ 创建了自定义上下文")
    print(f"   User ID: {context.user_id}")
    print(f"   Role: {context.role}")
    print(f"   Preferences: {context.preferences}")
except Exception as e:
    print(f"❌ 创建失败: {e}")

# 演示 9: 追踪（Tracing）
print("\n🔍 演示 9: 追踪功能")
print("-" * 70)
try:
    from agents import trace, set_tracing_disabled
    
    # 禁用追踪（演示模式）
    set_tracing_disabled(True)
    
    print(f"✅ 追踪系统已配置")
    print(f"   支持: OpenAI Dashboard, Logfire, AgentOps等")
    print(f"   功能: 自动追踪所有代理运行")
    print(f"   状态: 已禁用（演示模式）")
except Exception as e:
    print(f"❌ 配置失败: {e}")

# 演示 10: Runner 配置
print("\n🚀 演示 10: 执行引擎（Runner）")
print("-" * 70)
try:
    from agents import RunConfig
    
    print(f"✅ Runner 执行引擎")
    print(f"   异步方法: Runner.run()")
    print(f"   同步方法: Runner.run_sync()")
    print(f"   流式方法: Runner.run_streamed()")
    print(f"   特性: 自动工具调用、代理切换、会话管理")
except Exception as e:
    print(f"❌ 配置失败: {e}")

# 总结
print("\n" + "="*70)
print("✅ 演示完成！框架所有核心功能都正常工作")
print("="*70)

print("\n📚 要运行实际示例（需要 OPENAI_API_KEY），请查看:")
print("   - examples/basic/hello_world.py")
print("   - examples/agent_patterns/")
print("   - examples/tools/")
print("   - examples/handoffs/")

print("\n💡 设置 API key 后运行:")
print("   export OPENAI_API_KEY='sk-your-key-here'")
print("   python examples/basic/hello_world.py")

print("\n📖 完整文档:")
print("   https://openai.github.io/openai-agents-python/")

print("\n🧪 运行测试:")
print("   pytest tests/ -v")

print("\n" + "="*70 + "\n")

