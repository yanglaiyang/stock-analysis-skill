#!/usr/bin/env python3
"""
股票简化分析法 - 专业股票分析工具 (Subagent 架构版)
Stock Simplified Analysis Method (Subagent Architecture)

使用 Google Gemini AI + Tushare MCP 进行系统化的股票分析。
基于 7 步 Subagent 架构，每个步骤由专门的 AI 智能体负责。
"""

import os
import sys
import argparse
import time
from typing import Optional, List
import urllib.parse
import requests
from bs4 import BeautifulSoup

# 导入新的 Subagent 架构
from subagents import SubagentOrchestrator

# 系统提示词（用于测试与一致性校验）
SYSTEM_PROMPT = """
步骤一：业务增长周期分析
步骤二：业务分析
步骤三：护城河分析
步骤四：长期潜力分析
步骤五：关键指标分析
步骤六：风险分析
步骤七：估值分析

报告结构：
- 执行摘要
- 业务阶段分析
- 业务模式分析
- 护城河分析
- 长期增长潜力分析
- 关键指标健康检查
- 执行风险评估
- 估值框架分析
""".strip()


class StockAnalyzer:
    """股票分析器主类 (Subagent 架构封装)"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化分析器

        Args:
            api_key: Gemini API密钥
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("请设置 GEMINI_API_KEY 或 GOOGLE_API_KEY 环境变量")

        # 初始化 Orchestrator
        self.orchestrator = SubagentOrchestrator(self.api_key)
        print("✅ AI财务分析师已初始化（Subagent架构 + Tushare MCP），准备就绪。")

    def get_webpage_title(self, url: str) -> str:
        """获取网页或文件标题"""
        def _extract_filename(raw_url: str) -> str:
            decoded_url = urllib.parse.unquote(raw_url)
            clean_url = decoded_url.split('?', 1)[0]
            filename = clean_url.split('/')[-1]
            return filename.strip() if filename.strip() else "外部参考文档"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        try:
            response = requests.get(url, headers=headers, timeout=5, stream=True)
            if 'text/html' in response.headers.get('Content-Type', '').lower():
                response.encoding = response.apparent_encoding
                soup = BeautifulSoup(response.content, 'html.parser')
                if soup.title and soup.title.string:
                    return soup.title.string.strip()
            return _extract_filename(url)
        except Exception as e:
            print(f"⚠️ 无法抓取标题 ({url}): {e}")
            return _extract_filename(url)
        return "外部参考文档"

    def format_links(self, links: List[str]) -> str:
        """格式化链接列表为Markdown"""
        formatted_links = []
        for link in links:
            title = self.get_webpage_title(link)
            formatted_links.append(f"- [{title}]({link})")
        return "\n".join(formatted_links)

    def analyze(
        self,
        company: str,
        links: Optional[List[str]] = None,
        file_paths: Optional[List[str]] = None,
        output_file: Optional[str] = None,
        max_retries: int = 5
    ) -> str:
        """执行股票分析"""
        
        # 1. 处理输入数据
        pdf_content = ""
        if file_paths:
            print(f"📄 处理上传的文件: {len(file_paths)} 个")
            contents = []
            for fp in file_paths:
                if os.path.exists(fp):
                    try:
                        # 尝试使用 pdf_generator 中的工具或简单读取
                        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                             contents.append(f.read())
                    except Exception as e:
                        print(f"❌ 读取文件 {fp} 失败: {e}")
            pdf_content = "\n".join(contents)

        formatted_links = ""
        if links:
            formatted_links = self.format_links(links)
            if formatted_links:
                pdf_content += f"\n\n参考链接:\n{formatted_links}"

        # 2. 解析股票代码
        ts_code = None
        if ',' in company:
            parts = company.split(',')
            if len(parts) >= 2:
                ts_code = parts[1].strip()

        # 3. 运行 Subagent Orchestrator
        try:
            print(f"\n� 启动 Subagent 分析流程: {company}")
            if ts_code:
                print(f"🎯 股票代码: {ts_code}")
            
            report = self.orchestrator.run(
                company=company,
                ts_code=ts_code,
                pdf_content=pdf_content
            )
            
            # 4. 保存报告 (如果 run 方法返回的是文件路径)
            if output_file and report:
                # 检查是否已经是 HTML 文件
                if report.endswith('.html'):
                    # 如果用户指定了输出路径，且与默认生成的不一致，则移动或重命名
                    if output_file != report:
                        import shutil
                        shutil.move(report, output_file)
                        print(f"\n✅ 报告已保存至: {output_file}")
                        return output_file
                    else:
                        print(f"\n✅ 报告已保存至: {report}")
                        return report
                else:
                    # 传统的 Markdown 写入
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(report)
                    print(f"\n✅ 报告已保存至: {output_file}")
            
            return report

        except Exception as e:
            print(f"\n❌ 分析过程发生错误: {e}")
            import traceback
            traceback.print_exc()
            return ""


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='股票简化分析法 - 专业股票分析工具 (Subagent版)',
        formatter_class=argparse.RawDescriptionHelpFormatter
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
    parser.add_argument('--retries', type=int, default=5,
                        help='最大重试次数（默认: 5）')

    args = parser.parse_args()

    # 初始化并运行
    try:
        analyzer = StockAnalyzer(api_key=args.api_key)
        report = analyzer.analyze(
            company=args.company,
            links=[l.strip() for l in args.links.split(',')] if args.links else None,
            file_paths=args.files,
            output_file=args.output,
            max_retries=args.retries
        )
        
        if report:
            print("\n分析完成！")
        else:
            sys.exit(1)

    except Exception as e:
        print(f"❌ 程序运行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
