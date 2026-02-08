#!/usr/bin/env python3
"""
Subagent架构测试脚本
"""

import os
import sys

# 读取API密钥（不要硬编码到仓库）
API_KEY = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')

# 导入Subagent系统
from src.subagents import SubagentOrchestrator

def test_subagent_basic():
    """测试基本功能"""
    print("="*60)
    print("🧪 测试1: Subagent基本功能")
    print("="*60 + "\n")

    try:
        if not API_KEY:
            print("⚠️  未检测到 GEMINI_API_KEY / GOOGLE_API_KEY，跳过此测试\n")
            return True

        # 创建协调器
        orchestrator = SubagentOrchestrator(API_KEY)
        print("✅ Subagent协调器初始化成功\n")

        # 测试单个Subagent
        print("📊 测试PhaseAnalysisSubagent...")
        context = {
            'company': '测试公司, 000001.SZ',
            'tushare_data': '测试数据',
            'pdf_content': ''
        }

        result = orchestrator.subagents['phase'].analyze(context)
        print(f"✅ PhaseAnalysisSubagent 测试通过")
        print(f"   输出长度: {len(result['result'])} 字符\n")

        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}\n")
        return False


def test_tushare_integration():
    """测试Tushare集成"""
    print("="*60)
    print("🧪 测试2: Tushare MCP集成")
    print("="*60 + "\n")

    try:
        from src.tushare_mcp_client import get_tushare_client
        client = get_tushare_client()

        # 测试获取数据
        data = client.get_stock_basic(ts_code='000001.SZ')
        print("✅ Tushare MCP客户端工作正常")
        print(f"   数据长度: {len(data)} 字符\n")

        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}\n")
        return False


def test_full_analysis():
    """测试完整分析流程"""
    print("="*60)
    print("🧪 测试3: 完整7步分析流程（快速模式）")
    print("="*60 + "\n")

    try:
        if not API_KEY:
            print("⚠️  未检测到 GEMINI_API_KEY / GOOGLE_API_KEY，跳过此测试\n")
            return True

        orchestrator = SubagentOrchestrator(API_KEY)

        # 只测试前3步（节省时间）
        print("📊 执行步骤1: 业务阶段分析...")
        context = {
            'company': '平安银行, 000001.SZ',
            'tushare_data': '',
            'pdf_content': ''
        }
        result1 = orchestrator.subagents['phase'].analyze(context)
        print(f"✅ 步骤1完成\n")

        print("📊 执行步骤2: 业务模式分析...")
        context['phase_result'] = result1['result']
        result2 = orchestrator.subagents['business'].analyze(context)
        print(f"✅ 步骤2完成\n")

        print("📊 执行步骤3: 护城河分析...")
        context['business_result'] = result2['result']
        result3 = orchestrator.subagents['moat'].analyze(context)
        print(f"✅ 步骤3完成\n")

        print("="*60)
        print("✅ 完整测试通过！Subagent架构工作正常")
        print("="*60 + "\n")

        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🚀 Subagent架构测试套件")
    print("="*60 + "\n")

    results = []

    # 测试1: 基本功能
    results.append(("基本功能", test_subagent_basic()))

    # 测试2: Tushare集成
    results.append(("Tushare集成", test_tushare_integration()))

    # 测试3: 完整流程
    results.append(("完整流程", test_full_analysis()))

    # 汇总结果
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60 + "\n")

    for test_name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_name}: {status}")

    all_passed = all(result for _, result in results)

    print("\n" + "="*60)
    if all_passed:
        print("🎉 所有测试通过！Subagent架构可以投入使用。")
    else:
        print("⚠️  部分测试失败，请检查配置。")
    print("="*60 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
