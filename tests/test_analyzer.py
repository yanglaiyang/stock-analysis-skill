#!/usr/bin/env python3
"""
股票分析器测试文件
"""

import unittest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stock_analyzer import StockAnalyzer


class TestStockAnalyzer(unittest.TestCase):
    """StockAnalyzer测试类"""

    def setUp(self):
        """测试前设置"""
        # 注意：实际测试需要设置有效的API密钥
        self.api_key = os.getenv('GEMINI_API_KEY', 'test_key')

    def test_get_webpage_title_with_pdf(self):
        """测试PDF链接标题提取"""
        analyzer = StockAnalyzer(api_key=self.api_key)

        # 测试PDF链接
        pdf_url = "https://example.com/document.pdf"
        title = analyzer.get_webpage_title(pdf_url)
        self.assertEqual(title, "document.pdf")

    def test_get_webpage_title_with_complex_url(self):
        """测试复杂URL标题提取"""
        analyzer = StockAnalyzer(api_key=self.api_key)

        # 测试带参数的URL
        complex_url = "https://example.com/path/to/file.pdf?v=123&query=test"
        title = analyzer.get_webpage_title(complex_url)
        self.assertEqual(title, "file.pdf")

    def test_format_links(self):
        """测试链接格式化"""
        analyzer = StockAnalyzer(api_key=self.api_key)

        links = [
            "https://example.com/report1.pdf",
            "https://example.com/report2.pdf"
        ]

        formatted = analyzer.format_links(links)
        self.assertIn("report1.pdf", formatted)
        self.assertIn("report2.pdf", formatted)
        self.assertIn("](https://", formatted)

    def test_format_empty_links(self):
        """测试空链接列表"""
        analyzer = StockAnalyzer(api_key=self.api_key)

        formatted = analyzer.format_links([])
        self.assertEqual(formatted, "")


class TestAnalysisFramework(unittest.TestCase):
    """分析框架完整性测试"""

    def test_system_prompt_contains_all_steps(self):
        """测试系统提示词包含所有7个步骤"""
        from stock_analyzer import SYSTEM_PROMPT

        required_steps = [
            "步骤一：业务增长周期分析",
            "步骤二：业务分析",
            "步骤三：护城河分析",
            "步骤四：长期潜力分析",
            "步骤五：关键指标分析",
            "步骤六：风险分析",
            "步骤七：估值分析"
        ]

        for step in required_steps:
            self.assertIn(step, SYSTEM_PROMPT)

    def test_system_prompt_contains_report_structure(self):
        """测试系统提示词包含报告结构"""
        from stock_analyzer import SYSTEM_PROMPT

        required_sections = [
            "执行摘要",
            "业务阶段分析",
            "业务模式分析",
            "护城河分析",
            "长期增长潜力分析",
            "关键指标健康检查",
            "执行风险评估",
            "估值框架分析"
        ]

        for section in required_sections:
            self.assertIn(section, SYSTEM_PROMPT)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestStockAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestAnalysisFramework))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 返回结果
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
