#!/usr/bin/env python3
"""
股票分析器 - Subagent版本
使用7个专业化subagent进行分析
"""

import os
import sys
import argparse
from typing import List, Optional

# 导入subagent系统
from subagents import SubagentOrchestrator

# 导入Tushare MCP客户端
from tushare_mcp_client import get_tushare_client


class StockAnalyzerSubagent:
    """基于Subagent的股票分析器"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化分析器

        Args:
            api_key: Gemini API密钥
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("请设置 GEMINI_API_KEY 或 GOOGLE_API_KEY 环境变量")

        # 初始化Subagent协调器
        self.orchestrator = SubagentOrchestrator(self.api_key)

        # 初始化Tushare MCP客户端
        try:
            self.tushare_client = get_tushare_client()
            print("✅ 基于Subagent的分析器已初始化（Gemini AI + Tushare MCP）")
        except Exception as e:
            self.tushare_client = None
            print(f"⚠️  Tushare MCP客户端初始化失败: {e}")
            print("✅ 基于Subagent的分析器已初始化（Gemini AI）")

    def read_file_content(self, file_paths: List[str]) -> str:
        """读取文件内容"""
        file_contents = []

        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"❌ 文件不存在: {file_path}")
                continue

            print(f"   正在读取文件: {file_path} ...")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_contents.append(f"\n\n--- 文件: {os.path.basename(file_path)} ---\n{content}\n--- 文件结束 ---\n")
                    print(f"✅ {file_path} 读取完成。")
            except Exception as e:
                print(f"❌ 读取 {file_path} 时出错: {e}")

        return "\n".join(file_contents)

    def analyze(
        self,
        company: str,
        links: Optional[List[str]] = None,
        file_paths: Optional[List[str]] = None,
        output_file: Optional[str] = None
    ) -> str:
        """
        执行股票分析（使用subagent架构）

        Args:
            company: 公司名称和代码，如"平安银行, 000001.SZ"
            links: 参考链接列表
            file_paths: 上传的文件路径列表
            output_file: 输出报告文件路径

        Returns:
            分析报告文本
        """
        print(f"\n🎯 目标公司: {company}")
        print(f"📊 分析模式: Subagent架构（7个专业化agent）\n")

        # 读取文件内容
        pdf_content = ""
        if file_paths:
            pdf_content = self.read_file_content(file_paths)

        # 获取Tushare数据
        tushare_data = ""
        ts_code = None
        if ',' in company:
            parts = company.split(',')
            if len(parts) >= 2:
                ts_code = parts[1].strip()
                if self.tushare_client:
                    tushare_data = self.tushare_client.get_all_data(ts_code)

        # 显示数据源优先级
        print("\n" + "="*60)
        print("📊 数据源优先级")
        print("="*60)
        if pdf_content:
            print("🥇 第一优先级: 用户上传的PDF文件 ✅")
            print("🥈 第二优先级: Tushare MCP实时数据 ✅" if tushare_data else "🥈 第二优先级: Tushare MCP实时数据 ❌")
        else:
            print("🥇 第一优先级: Tushare MCP实时数据 ✅" if tushare_data else "🥇 第一优先级: Tushare MCP实时数据 ❌")
        print("="*60 + "\n")

        # 运行subagent分析并生成HTML报告（默认）
        print("\n" + "="*60)
        print("📊 正在生成完整HTML报告（含图表）")
        print("="*60 + "\n")

        html_file = self.orchestrator.run(
            company=company,
            ts_code=ts_code,
            pdf_content=pdf_content
        )

        print(f"\n✅ HTML报告已生成: {html_file}")

        # 如果用户指定了输出文件且是.md格式，则额外生成Markdown版本
        if output_file and output_file.endswith('.md'):
            print(f"\n📝 正在生成Markdown版本...")
            results = self.orchestrator.run_analysis(
                company=company,
                tushare_data=tushare_data,
                pdf_content=pdf_content
            )
            report = self.orchestrator.generate_final_report(company, results)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Markdown报告已保存至: {output_file}")

            return report

        return html_file


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='股票简化分析法 - Subagent版本（7个专业化agent）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析平安银行（使用subagent架构）
  python stock_analyzer_subagent.py -c "平安银行, 000001.SZ"

  # 分析并指定输出文件
  python stock_analyzer_subagent.py -c "宁德时代, 300750" -o report.md

  # 上传券商研报（PDF为第一优先级）
  python stock_analyzer_subagent.py -c "贵州茅台, 600519" -f research_report.pdf

  # 组合使用
  python stock_analyzer_subagent.py -c "比亚迪, 002594" \\
    -f report.pdf -o report.md

架构说明:
  - 使用7个专业化subagent分别执行各步骤分析
  - Subagent 1: 业务阶段分析
  - Subagent 2: 业务模式分析
  - Subagent 3: 护城河分析
  - Subagent 4: 增长潜力分析
  - Subagent 5: 关键指标分析
  - Subagent 6: 风险评估
  - Subagent 7: 估值框架分析
        """
    )

    parser.add_argument('-c', '--company', required=True,
                        help='公司名称和代码，格式: "公司名, 代码"')
    parser.add_argument('-l', '--links',
                        help='参考链接（用逗号分隔）')
    parser.add_argument('-f', '--files', nargs='+',
                        help='上传的文件路径（支持多个）')
    parser.add_argument('-o', '--output',
                        help='输出报告文件路径（Markdown格式）')
    parser.add_argument('-k', '--api-key',
                        help='Gemini API密钥')

    args = parser.parse_args()

    # 检查API密钥
    api_key = args.api_key
    if not api_key:
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if not api_key:
            api_key = os.getenv('ANTHROPIC_AUTH_TOKEN')
            if api_key:
                print("⚠️  使用 ANTHROPIC_AUTH_TOKEN 作为 API 密钥")
            else:
                print("❌ 错误: 请设置 GEMINI_API_KEY 环境变量或使用 -k 参数")
                print("\n获取 API 密钥:")
                print("  1. 访问 https://aistudio.google.com/app/apikey")
                print("  2. 创建新的 API 密钥")
                print("  3. 设置环境变量: export GEMINI_API_KEY='your_api_key'")
                sys.exit(1)

    # 初始化分析器
    try:
        analyzer = StockAnalyzerSubagent(api_key=api_key)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # 处理链接
    links = None
    if args.links:
        links = [link.strip() for link in args.links.split(',') if link.strip()]

    # 执行分析
    report = analyzer.analyze(
        company=args.company,
        links=links,
        file_paths=args.files,
        output_file=args.output
    )

    if report:
        print("\n" + "="*60)
        print("✅ 分析完成！")
        print("="*60)
        print(f"\n📄 报告文件: {report}")
        print("\n💡 提示:")
        print("  - 双击HTML文件在浏览器中查看完整报告")
        print("  - 报告包含15种专业图表和完整分析")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
