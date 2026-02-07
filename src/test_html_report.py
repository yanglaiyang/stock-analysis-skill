"""
测试HTML报告生成功能
生成包含图表的完整HTML报告
"""

import sys
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent))

from html_report_generator import HtmlReportGenerator
from chart_generator import StockChartGenerator
from font_config import configure_chinese_font


def test_html_report_with_charts():
    """测试生成包含图表的HTML报告"""

    print("\n" + "="*70)
    print(" "*20 + "HTML报告生成测试")
    print("="*70)

    # 1. 配置字体
    print("\n步骤 1/5: 配置中文字体...")
    configure_chinese_font()

    # 2. 创建图表生成器
    print("\n步骤 2/5: 创建图表...")
    chart_gen = StockChartGenerator(output_dir='test_output/html_test_charts', verbose=True)

    # 生成测试图表
    test_scores = {
        '业务阶段': 85,
        '护城河': 90,
        '财务健康': 85,
        '增长潜力': 65,
        '风险控制': 60
    }

    radar_chart = chart_gen.create_investment_radar(test_scores)

    # 3. 准备报告内容
    print("\n步骤 3/5: 准备报告内容...")
    report_content = f"""
# 📊 测试公司投资分析报告

## 🎯 投资评级: ⭐⭐⭐☆☆ 买入

根据综合分析，我们给予该公司 **买入** 评级。

---

## 📊 投资评分仪表盘

CHART_INVESTMENT_RADAR

---

## 💰 核心财务数据

| 指标 | 数值 | 评级 | 趋势 |
|------|------|------|------|
| 营业收入 | 180.90亿元 | 🟢 优秀 | 稳定 |
| 毛利率 | 71.10% | 🟢 优秀 | 稳定 |
| 净利率 | 21.90% | 🟢 优秀 | 稳定 |
| ROE | 7.94% | 🟡 良好 | 需观察 |
| 资产负债率 | 18.22% | 🟢 极佳 | 稳定 |

---

## 💎 投资建议

<div class="recommendation-box">
<h3>建议: 逢低买入</h3>
<p><strong>目标价:</strong> 180-200元</p>
<p><strong>止损价:</strong> 120元</p>
<p><strong>持仓周期:</strong> 12-24个月</p>
</div>

### 核心理由

1. 低估值（PE=12.46）提供安全边际
2. 高毛利（71.10%）和高净利（21.90%）盈利质量优秀
3. 强品牌带来稳定现金流
4. 成熟期适合价值投资

---

## ⚠️ 风险提示

> 投资有风险，入市需谨慎。本报告仅供参考，不构成投资建议。

### 主要风险

- **集中度风险** 🔴: 业务100%依赖白酒产品
- **政策风险** 🔴: 政府政策监管风险
- **竞争风险** 🔴: 白酒行业竞争白热化

---

## 📌 数据来源

- Tushare MCP实时数据
- 公司公开财报
- 行业研究报告

---

**分析方法**: Subagent架构（7个专业化AI Agent）
**生成时间**: 2026年02月07日
"""

    # 4. 生成HTML报告
    print("\n步骤 4/5: 生成HTML报告...")
    html_gen = HtmlReportGenerator(output_dir='test_output')

    output_file = html_gen.generate_report(
        markdown_content=report_content,
        chart_paths={
            'CHART_INVESTMENT_RADAR': radar_chart,
        },
        output_path='test_output/测试报告_完整版.html',
        title='测试公司投资分析报告'
    )

    # 5. 显示结果
    print("\n步骤 5/5: 验证结果...")
    if output_file and Path(output_file).exists():
        file_size = Path(output_file).stat().st_size / 1024
        print(f"\n{'='*70}")
        print("✅ HTML报告生成成功！")
        print(f"{'='*70}")
        print(f"文件路径: {output_file}")
        print(f"文件大小: {file_size:.1f} KB")
        print(f"包含图表: 1 张")
        print(f"\n请用浏览器打开查看效果:")
        print(f"  open {output_file}")
        print(f"{'='*70}\n")
        return True
    else:
        print("\n❌ HTML报告生成失败")
        return False


if __name__ == '__main__':
    success = test_html_report_with_charts()
    sys.exit(0 if success else 1)
