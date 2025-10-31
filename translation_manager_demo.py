#!/usr/bin/env python3
"""
语言翻译 Manager Agent 演示
演示如何使用 Manager 模式（Agents as Tools）来协调多个翻译代理
"""
import asyncio
import os

from agents import Agent, ItemHelpers, MessageOutputItem, Runner, trace

print("\n" + "="*70)
print("🌍 语言翻译 Manager Agent 演示")
print("="*70)
print("\n这个示例展示 'Manager模式' (也叫 Orchestrator模式)")
print("一个中心管理器代理调用多个专业翻译代理作为工具\n")

# ========== 创建专业翻译代理 ==========

spanish_agent = Agent(
    name="西班牙语翻译专家",
    instructions="你是专业的英语到西班牙语翻译，准确地翻译用户的消息到西班牙语。",
    handoff_description="英语到西班牙语的专业翻译",
)

french_agent = Agent(
    name="法语翻译专家",
    instructions="你是专业的英语到法语翻译，准确地翻译用户的消息到法语。",
    handoff_description="英语到法语的专业翻译",
)

italian_agent = Agent(
    name="意大利语翻译专家",
    instructions="你是专业的英语到意大利语翻译，准确地翻译用户的消息到意大利语。",
    handoff_description="英语到意大利语的专业翻译",
)

chinese_agent = Agent(
    name="中文翻译专家",
    instructions="你是专业的英语到中文翻译，准确地翻译用户的消息到简体中文。",
    handoff_description="英语到中文的专业翻译",
)

# ========== 创建管理器/编排器代理 ==========

orchestrator_agent = Agent(
    name="翻译管理器",
    instructions=(
        "你是一个翻译管理器。你使用提供的工具来完成翻译任务。"
        "如果用户要求多种语言的翻译，你要按顺序调用相关的工具。"
        "你从不自己翻译，而是始终使用提供的工具来完成翻译。"
        "对每种语言的翻译，要清楚标注是哪种语言。"
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
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="将用户的消息翻译成意大利语",
        ),
        chinese_agent.as_tool(
            tool_name="translate_to_chinese",
            tool_description="将用户的消息翻译成中文",
        ),
    ],
)

# ========== 创建合成器代理（可选） ==========

synthesizer_agent = Agent(
    name="翻译合成器",
    instructions=(
        "你检查各种语言的翻译，必要时进行修正，"
        "并产生一个最终的、格式良好的综合响应。"
        "确保每个翻译都有清晰的语言标签。"
    ),
)


async def translate_with_manager(text: str, use_synthesizer: bool = True):
    """
    使用 Manager 模式进行翻译
    
    Args:
        text: 要翻译的文本
        use_synthesizer: 是否使用合成器代理来整理输出
    """
    print(f"\n📝 输入文本: \"{text}\"")
    print("-" * 70)
    
    # 在单个追踪中运行整个编排
    with trace("Translation Orchestration"):
        print("\n🔄 管理器代理正在协调翻译...")
        orchestrator_result = await Runner.run(orchestrator_agent, text)
        
        # 显示中间步骤
        print("\n📋 翻译步骤:")
        for i, item in enumerate(orchestrator_result.new_items, 1):
            if isinstance(item, MessageOutputItem):
                text_content = ItemHelpers.text_message_output(item)
                if text_content:
                    print(f"  步骤 {i}: {text_content[:100]}...")
        
        if use_synthesizer:
            print("\n✨ 合成器代理正在整理输出...")
            synthesizer_result = await Runner.run(
                synthesizer_agent, orchestrator_result.to_input_list()
            )
            final_output = synthesizer_result.final_output
        else:
            final_output = orchestrator_result.final_output
    
    print("\n" + "="*70)
    print("📤 最终结果:")
    print("="*70)
    print(f"\n{final_output}\n")
    
    return final_output


async def demo_without_api_key():
    """无需API密钥的演示（展示架构）"""
    print("\n💡 架构说明:")
    print("-" * 70)
    print(f"\n✅ 已创建 {len(orchestrator_agent.tools)} 个翻译工具:")
    for i, tool in enumerate(orchestrator_agent.tools, 1):
        print(f"  {i}. {tool.name} - {tool.description}")
    
    print(f"\n✅ 管理器代理: {orchestrator_agent.name}")
    print(f"   - 工具数量: {len(orchestrator_agent.tools)}")
    print(f"   - 角色: 协调和调用专业翻译代理")
    
    print(f"\n✅ 合成器代理: {synthesizer_agent.name}")
    print(f"   - 角色: 检查和整理最终输出")
    
    print("\n📊 工作流程:")
    print("  1. 用户输入文本和目标语言")
    print("  2. 管理器代理分析请求")
    print("  3. 管理器调用相应的翻译工具")
    print("  4. 每个专业代理完成翻译")
    print("  5. 合成器整理所有翻译")
    print("  6. 返回格式化的结果")
    
    print("\n💡 这是 'Manager模式' 的典型应用:")
    print("   - 一个中心管理器控制整个对话")
    print("   - 专业代理作为工具被调用")
    print("   - 管理器始终保持控制权")
    print("   - 适合需要协调多个专家的场景")


async def demo_with_api_key():
    """需要API密钥的实际演示"""
    print("\n🚀 开始实际翻译演示...")
    print("="*70)
    
    # 示例 1: 单语言翻译
    print("\n示例 1: 翻译成西班牙语")
    await translate_with_manager(
        "Translate this to Spanish: Hello, how are you?",
        use_synthesizer=False
    )
    
    # 示例 2: 多语言翻译
    print("\n示例 2: 翻译成多种语言")
    await translate_with_manager(
        "Translate 'Good morning' to Spanish, French, and Italian",
        use_synthesizer=True
    )
    
    # 示例 3: 中文翻译
    print("\n示例 3: 翻译成中文")
    await translate_with_manager(
        "Translate 'Artificial Intelligence is transforming the world' to Chinese",
        use_synthesizer=False
    )


async def main():
    """主函数"""
    # 检查是否有API密钥
    has_api_key = bool(os.getenv("OPENAI_API_KEY"))
    
    if has_api_key:
        print("\n✅ 检测到 OPENAI_API_KEY，将运行实际演示")
        try:
            await demo_with_api_key()
        except Exception as e:
            print(f"\n❌ 运行出错: {e}")
            print("\n💡 如果API密钥无效，请设置正确的密钥:")
            print("   export OPENAI_API_KEY='sk-your-api-key-here'")
    else:
        print("\n⚠️  未检测到 OPENAI_API_KEY，将运行架构演示")
        await demo_without_api_key()
        
        print("\n" + "="*70)
        print("💡 要运行实际翻译演示，请设置 API 密钥:")
        print("="*70)
        print("\n  export OPENAI_API_KEY='sk-your-api-key-here'")
        print("  python translation_manager_demo.py")
    
    print("\n" + "="*70)
    print("📚 相关文档和示例:")
    print("="*70)
    print("\n  - 官方示例: examples/agent_patterns/agents_as_tools.py")
    print("  - 条件工具: examples/agent_patterns/agents_as_tools_conditional.py")
    print("  - 路由模式: examples/agent_patterns/routing.py")
    print("  - 中文文档: docs/zh/agents.md")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

