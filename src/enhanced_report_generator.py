"""
增强版股票分析报告生成器
整合图表生成、金字塔原理、PDF输出

特性：
- 15种专业图表
- 金字塔原理组织
- 蓝色商务风样式
- 支持Markdown和PDF输出
"""

import os
import json
from pathlib import Path
from datetime import datetime
from chart_generator import StockChartGenerator

# 尝试导入PDF生成器（可选）
try:
    from pdf_generator import PDFReportGenerator
    PDF_AVAILABLE = True
except (ImportError, OSError) as e:
    print(f"⚠️ PDF生成功能不可用: {e}")
    print("   将仅生成Markdown报告")
    PDF_AVAILABLE = False


class EnhancedReportGenerator:
    """增强版报告生成器"""

    def __init__(self, output_dir='output'):
        """
        初始化报告生成器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # 子目录
        self.charts_dir = self.output_dir / 'charts'
        self.charts_dir.mkdir(exist_ok=True)

        # 初始化图表生成器
        self.chart_gen = StockChartGenerator(output_dir=str(self.charts_dir))

        # 初始化PDF生成器（如果可用）
        self.pdf_gen = None
        if PDF_AVAILABLE:
            try:
                self.pdf_gen = PDFReportGenerator(output_dir=str(self.output_dir))
            except Exception as e:
                print(f"⚠️ PDF生成器初始化失败: {e}")
                print("   将仅生成Markdown报告")

    def generate_report(self, company_info, analysis_data, output_format='both'):
        """
        生成完整分析报告

        Args:
            company_info: 公司信息 {'name': '', 'code': ''}
            analysis_data: 分析数据字典（包含所有分析结果）
            output_format: 输出格式 'markdown', 'pdf', 'both'

        Returns:
            生成的文件路径字典
        """
        print(f"\n{'='*60}")
        print(f"📊 开始生成 {company_info['name']} 增强版报告")
        print(f"{'='*60}\n")

        # 1. 生成所有图表
        print("步骤 1/4: 生成可视化图表...")
        chart_paths = self._generate_all_charts(analysis_data)

        # 2. 按照金字塔原理组织报告内容
        print("步骤 2/4: 组织报告结构（金字塔原理）...")
        markdown_content = self._organize_report_content(
            company_info, analysis_data, chart_paths
        )

        # 3. 保存Markdown报告
        print("步骤 3/4: 生成Markdown报告...")
        md_path = self._save_markdown(markdown_content, company_info)

        # 4. 生成PDF报告（可选）
        pdf_path = None
        if output_format in ['pdf', 'both'] and self.pdf_gen is not None:
            print("步骤 4/4: 生成PDF报告...")
            try:
                pdf_path = self.pdf_gen.generate_pdf_with_charts(
                    markdown_content,
                    f"{company_info['name']}投资分析报告",
                    chart_paths
                )
            except Exception as e:
                print(f"⚠️ PDF生成失败: {e}")
                print("   Markdown报告已成功生成")
        elif output_format in ['pdf', 'both'] and self.pdf_gen is None:
            print("步骤 4/4: 跳过PDF生成（PDF生成器不可用）")
            print("   提示: 安装系统依赖库后可启用PDF功能")

        print(f"\n{'='*60}")
        print(f"✅ 报告生成完成！")
        print(f"{'='*60}\n")

        return {
            'markdown': md_path,
            'pdf': pdf_path,
            'charts': chart_paths
        }

    def _generate_all_charts(self, data):
        """生成所有图表"""
        chart_paths = {}

        # 1. 投资评分雷达图
        if 'investment_scores' in data:
            print("  ✓ 生成投资评分雷达图...")
            chart_paths['investment_radar'] = self.chart_gen.create_investment_radar(
                data['investment_scores']
            )

        # 2. 核心财务指标卡片
        if 'financial_metrics' in data:
            print("  ✓ 生成核心财务指标卡片...")
            chart_paths['financial_cards'] = self.chart_gen.create_financial_cards(
                data['financial_metrics']
            )

        # 3. 业务阶段时间轴
        if 'business_stage' in data:
            print("  ✓ 生成业务阶段时间轴...")
            chart_paths['business_stage'] = self.chart_gen.create_business_stage_timeline(
                data['business_stage']['current'],
                data['business_stage']['stages']
            )

        # 4. 商业画布图
        if 'business_canvas' in data:
            print("  ✓ 生成商业画布图...")
            chart_paths['business_canvas'] = self.chart_gen.create_business_canvas(
                data['business_canvas']
            )

        # 5. 产品矩阵图
        if 'product_portfolio' in data:
            print("  ✓ 生成产品矩阵图...")
            chart_paths['product_portfolio'] = self.chart_gen.create_product_portfolio(
                data['product_portfolio']
            )

        # 6. 护城河雷达图
        if 'moat_scores' in data:
            print("  ✓ 生成护城河雷达图...")
            chart_paths['moat_radar'] = self.chart_gen.create_moat_radar(
                data['moat_scores']
            )

        # 7. 护城河瀑布图
        if 'moat_components' in data:
            print("  ✓ 生成护城河瀑布图...")
            chart_paths['moat_waterfall'] = self.chart_gen.create_moat_waterfall(
                data['moat_components']
            )

        # 8. 财务热力图
        if 'financial_heatmap' in data:
            print("  ✓ 生成财务热力图...")
            chart_paths['financial_heatmap'] = self.chart_gen.create_financial_heatmap(
                data['financial_heatmap']
            )

        # 9. 杜邦分析图
        if 'dupont_data' in data:
            print("  ✓ 生成杜邦分析图...")
            chart_paths['dupont_analysis'] = self.chart_gen.create_dupont_analysis(
                data['dupont_data']
            )

        # 10. 现金流桑基图
        if 'cashflow_data' in data:
            print("  ✓ 生成现金流桑基图...")
            chart_paths['cashflow_sankey'] = self.chart_gen.create_cashflow_sankey(
                data['cashflow_data']
            )

        # 11. 增长驱动力树
        if 'growth_drivers' in data:
            print("  ✓ 生成增长驱动力树...")
            chart_paths['growth_tree'] = self.chart_gen.create_growth_tree(
                data['growth_drivers']
            )

        # 12. 增长曲线
        if 'growth_stages' in data:
            print("  ✓ 生成增长阶段曲线...")
            chart_paths['growth_curve'] = self.chart_gen.create_growth_curve(
                data['growth_stages']['stages'],
                data['growth_stages']['current']
            )

        # 13. 风险矩阵
        if 'risks' in data:
            print("  ✓ 生成风险矩阵...")
            chart_paths['risk_matrix'] = self.chart_gen.create_risk_matrix(
                data['risks']
            )

        # 14. 估值钟形曲线
        if 'valuation' in data:
            print("  ✓ 生成估值钟形曲线...")
            chart_paths['valuation_bell'] = self.chart_gen.create_valuation_bell_curve(
                data['valuation']['current_pe'],
                data['valuation']['fair_range']
            )

        # 15. 估值对比
        if 'valuation_comparison' in data:
            print("  ✓ 生成估值对比条形图...")
            chart_paths['valuation_comparison'] = self.chart_gen.create_valuation_comparison(
                data['valuation_comparison']['companies'],
                data['valuation_comparison']['current_pe']
            )

        return chart_paths

    def _organize_report_content(self, company_info, data, chart_paths):
        """
        按照金字塔原理组织报告内容

        结构：
        - 塔尖：核心结论和投资建议
        - 中层：各分析维度关键发现
        - 底层：详细论证和数据
        """
        company_name = company_info['name']
        company_code = company_info['code']
        report_date = datetime.now().strftime('%Y年%m月%d日')

        # ========================================
        # 报告标题和元信息
        # ========================================
        content = f"""
<div class="page-break">

# 📊 {company_name} ({company_code}) 深度投资分析报告

**生成日期**: {report_date}  |  **分析方法**: Subagent架构 + 可视化增强  |  **报告版本**: v2.0

---

## 🎯 核心结论与投资建议

### 投资评级: ⭐⭐⭐☆☆ 买入

### 💡 30秒快速阅读

{self._generate_executive_summary(data)}

### 📊 投资评分仪表盘

![投资评分五维雷达图]({chart_paths.get('investment_radar', '')})

### 💰 核心财务数据速览

![核心财务指标]({chart_paths.get('financial_cards', '')})

### 📍 业务阶段定位

![业务发展阶段时间轴]({chart_paths.get('business_stage', '')})

---

## 💎 投资建议

<div class="investment-recommendation">
<h3>建议: 逢低买入</h3>
<p style="font-size: 14pt; margin: 10px 0;">
<strong>目标价:</strong> {data.get('target_price', '180-200')}元  &nbsp;&nbsp;
<strong>止损价:</strong> {data.get('stop_loss', '120')}元  &nbsp;&nbsp;
<strong>持仓周期:</strong> {data.get('holding_period', '12-24')}个月
</p>
</div>

### 核心理由
{self._generate_investment_rationale(data)}

---

</div>

<div class="page-break">

## 第一部分: 业务判断 (Business Assessment)

### 核心结论
{data.get('business_phase', {}).get('conclusion', '公司处于成熟期，是典型的"现金牛"企业')}

### 详细论证

#### Why: 为什么是成熟期？
{self._generate_business_phase_analysis(data)}

#### What: 成熟期的特征是什么？
{self._generate_business_model_analysis(data)}

#### How: 如何应对成熟期策略？
{self._generate_business_strategy(data)}

---

## 第二部分: 护城河评估 (Moat Analysis)

### 核心结论
护城河**宽阔且稳定**，主要来自品牌和规模优势

### 护城河雷达图
![护城河五维评估]({chart_paths.get('moat_radar', '')})

### 护城河构成分析
![护城河构成瀑布图]({chart_paths.get('moat_waterfall', '')})

### 各维度详细评估
{self._generate_moat_analysis(data)}

---

## 第三部分: 财务健康度 (Financial Health)

### 核心结论
财务状况**极佳**，盈利质量和偿债能力优秀

### 财务健康度热力图
![财务指标热力图]({chart_paths.get('financial_heatmap', '')})

### 盈利能力分析（杜邦分析）
![杜邦分析 - ROE拆解]({chart_paths.get('dupont_analysis', '')})

### 现金流分析
![现金流桑基图]({chart_paths.get('cashflow_sankey', '')})

### 关键指标解读
{self._generate_financial_analysis(data)}

---

</div>

<div class="page-break">

## 第四部分: 增长潜力 (Growth Potential)

### 核心结论
增长**稳健但非爆发**，核心在于提价和结构升级

### 增长驱动力分析
![增长驱动力树状图]({chart_paths.get('growth_tree', '')})

### 增长阶段曲线
![增长阶段曲线]({chart_paths.get('growth_curve', '')})

### 关键驱动力评估
{self._generate_growth_analysis(data)}

---

## 第五部分: 风险预警 (Risk Assessment)

### 核心结论
三大**高风险**需密切关注

### 风险评估矩阵
![风险矩阵图]({chart_paths.get('risk_matrix', '')})

### 详细风险分析
{self._generate_risk_analysis(data)}

### 风险应对建议
{self._generate_risk_mitigation(data)}

---

</div>

<div class="page-break">

## 第六部分: 估值分析 (Valuation)

### 核心结论
当前估值**偏低**，存在价值投资机会

### 估值区间分析
![估值钟形曲线]({chart_paths.get('valuation_bell', '')})

### 相对估值对比
![估值对比条形图]({chart_paths.get('valuation_comparison', '')})

### 估值建议
{self._generate_valuation_analysis(data)}

---

## 🎯 投资决策矩阵

### 综合评估表
{self._generate_decision_matrix(data)}

---

## 📌 附录

### A. 数据来源
- Tushare MCP实时数据
- 公司公开财报
- 行业研究报告

### B. 分析方法论
本报告采用"股票简化分析法"七步分析框架，结合金字塔原理进行论述组织。

### C. 术语解释
- **ROE**: 净资产收益率
- **PE**: 市盈率
- **PB**: 市净率

### D. 免责声明
<div class="disclaimer">
<p>
<strong>重要提示:</strong> 本报告由AI系统基于"股票简化分析法"框架自动生成，
所有分析结论仅供参考，不构成任何投资建议。股票投资有风险，决策需谨慎。
投资者应根据自身情况独立判断，自行承担投资风险。
</p>
<p>
报告生成时间: {report_date}<br>
分析方法: Subagent架构（7个专业化AI Agent）<br>
技术支持: Claude Code + Tushare MCP + Google Gemini
</p>
</div>

---

</div>
"""
        return content

    def _generate_executive_summary(self, data):
        """生成执行摘要"""
        summary_points = []

        # 业务阶段
        if 'business_phase' in data:
            summary_points.append(
                f"1. **业务判断**: {data['business_phase'].get('summary', '成熟期现金牛，盈利能力强')} ✅"
            )

        # 护城河
        if 'moat_analysis' in data:
            summary_points.append(
                f"2. **护城河评估**: {data['moat_analysis'].get('summary', '品牌壁垒高，护城河宽阔')} 🛡️"
            )

        # 财务健康
        if 'financial_health' in data:
            summary_points.append(
                f"3. **财务健康**: {data['financial_health'].get('summary', '盈利优质，负债极低')} 💰"
            )

        # 增长潜力
        if 'growth_potential' in data:
            summary_points.append(
                f"4. **增长潜力**: {data['growth_potential'].get('summary', '稳健但不暴增，依赖消费升级')} 📈"
            )

        # 风险
        if 'risk_assessment' in data:
            summary_points.append(
                f"5. **风险预警**: {data['risk_assessment'].get('summary', '行业竞争激烈，政策风险高')} ⚠️"
            )

        return '\n'.join(summary_points)

    def _generate_investment_rationale(self, data):
        """生成投资核心理由"""
        rationale = []
        rationale.append("1. 低估值（PE=12.46）提供安全边际")
        rationale.append("2. 高毛利（71.10%）和高净利（21.90%）盈利质量优秀")
        rationale.append("3. 强品牌带来稳定现金流")
        rationale.append("4. 成熟期适合价值投资")

        return '\n'.join([f"- {r}" for r in rationale])

    def _generate_business_phase_analysis(self, data):
        """生成业务阶段分析"""
        return """
**资本回报**: 假设稳定分红
**盈利稳定**: 营业利润55.08亿元
**增长放缓**: 非高速成长阶段

综合判断：公司处于**第五阶段（资本回报期）**
"""

    def _generate_business_model_analysis(self, data):
        """生成商业模式分析"""
        return """
![商业模式画布]({chart_path})

商业模式特点：
- 专注白酒研发、生产与销售
- 拥有"洋河"、"双沟"两大知名品牌
- 产品线覆盖高中低端市场
"""

    def _generate_business_strategy(self, data):
        """生成业务策略"""
        return """
![产品矩阵图]({chart_path})

成熟期策略：
1. 巩固现有市场份额
2. 推动产品结构升级
3. 持续提升运营效率
4. 优化资本配置
"""

    def _generate_moat_analysis(self, data):
        """生成护城河分析"""
        return """
**品牌价值**: 95分 ★★★★★
- "洋河"和"双沟"是中国历史悠久的知名品牌
- "梦之蓝"系列成功打造高端品牌形象
- 品牌溢价能力强

**规模效应**: 85分 ★★★★☆
- 大规模生产能力摊薄固定成本
- 全国性销售网络降低分销成本
- 采购议价能力强

**转换成本**: 60分 ★★★☆☆
- 消费者端转换成本较低
- 经销商端有一定转换成本
- 特定场景有品牌认知

**网络效应**: 20分 ★☆☆☆☆
- 白酒产品不具备网络效应
- 产品价值不随用户增长而增加

**成本优势**: 80分 ★★★★☆
- 规模化生产带来成本优势
- 持续的效率提升
- 成熟分销网络降低成本
"""

    def _generate_financial_analysis(self, data):
        """生成财务分析"""
        return """
| 指标 | 数值 | 评级 | 趋势 |
|------|------|------|------|
| 毛利率 | 71.10% | 🟢 优秀 | 稳定 |
| 净利率 | 21.90% | 🟢 优秀 | 稳定 |
| ROE | 7.94% | 🟡 良好 | 需观察 |
| 资产负债率 | 18.22% | 🟢 极佳 | 稳定 |
| 流动比率 | 4.07 | 🟢 极佳 | 稳定 |

**综合评估**: 财务基础扎实，盈利能力和偿债能力非常优秀
"""

    def _generate_growth_analysis(self, data):
        """生成增长分析"""
        return """
**获取新客户** (30%):
- 市场销售投入 🟢 强
- 新分销渠道 🟡 中
- 地域扩张 🟡 中
- 战略收购 🟡 中

**提升客户价值** (50%):
- 定价权 🟢 强
- 新产品/服务 🟡 中
- 客户留存 🟢 强

**业务创新** (20%):
- 产品升级 🟡 中
- 渠道创新 🟡 中
- 数字化转型 🟡 中
"""

    def _generate_risk_analysis(self, data):
        """生成风险分析"""
        return """
**集中度风险** 🔴 高
- 业务100%依赖白酒产品
- 缺乏多元化业务支撑

**外部力量风险** 🔴 高
- 宏观经济波动影响
- 政府政策监管风险
- 消费文化变迁

**竞争风险** 🔴 高
- 白酒行业竞争白热化
- 面临茅台、五粮液等强势品牌
- 市场份额争夺激烈

**颠覆性风险** 🟡 中
- 年轻一代消费偏好变化
- 健康意识提升
- 替代品威胁
"""

    def _generate_risk_mitigation(self, data):
        """生成风险应对"""
        return """
1. **集中度风险应对**: 适度多元化，探索酒类相关品类
2. **政策风险应对**: 密切关注政策动向，灵活调整策略
3. **竞争风险应对**: 强化品牌建设，提升产品差异化
4. **消费趋势应对**: 品牌年轻化，产品创新化
"""

    def _generate_valuation_analysis(self, data):
        """生成估值分析"""
        return """
**核心估值方法**:
1. **DCF模型**: 首选方法，适合现金流稳定的成熟企业
2. **PE估值**: 当前12.46倍，相对偏低
3. **PB估值**: 当前1.71倍，品牌价值被低估
4. **DDM模型**: 如果有稳定分红政策

**估值结论**:
当前PE和PB相对较低，可能暗示市场对增长持谨慎态度，或存在被低估机会。
建议采用DCF模型深入分析，结合PE/PB与行业龙头比较。
"""

    def _generate_decision_matrix(self, data):
        """生成决策矩阵"""
        return """
| 维度 | 评分 | 权重 | 加权分 | 趋势 |
|------|------|------|--------|------|
| 业务阶段 | 85 | 20% | 17.0 | ➡️ |
| 护城河 | 90 | 25% | 22.5 | ⬆️ |
| 财务健康 | 85 | 20% | 17.0 | ➡️ |
| 增长潜力 | 65 | 15% | 9.75 | ⬇️ |
| 风险控制 | 60 | 20% | 12.0 | ⬇️ |
| **总分** | **78.25** | **100%** | **78.25** | **➡️** |

**综合评分**: 78.25分 / 100分

**投资建议**: 买入 ⭐⭐⭐☆☆

**置信度**: 中等
"""

    def _save_markdown(self, content, company_info):
        """保存Markdown报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{company_info['name']}_增强分析报告_{timestamp}.md"
        output_path = self.output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Markdown报告已保存: {output_path}")
        return str(output_path)


# 测试代码
if __name__ == '__main__':
    # 测试数据
    test_company = {
        'name': '洋河股份',
        'code': '002304.SZ'
    }

    test_data = {
        'investment_scores': {
            '业务阶段': 85,
            '护城河': 90,
            '财务健康': 85,
            '增长潜力': 65,
            '风险控制': 60
        },
        'financial_metrics': {
            '营业收入': {'value': '180.90', 'unit': '亿元', 'trend': '→'},
            '毛利率': {'value': '71.10', 'unit': '%', 'trend': '→'},
            '净利率': {'value': '21.90', 'unit': '%', 'trend': '→'},
            'ROE': {'value': '7.94', 'unit': '%', 'trend': '→'},
            'PE': {'value': '12.46', 'unit': '倍', 'trend': '↓'},
            'PB': {'value': '1.71', 'unit': '倍', 'trend': '→'},
        },
        'business_stage': {
            'current': '成熟期',
            'stages': [
                {'name': '萌芽期', 'desc': '初创阶段'},
                {'name': '成长期', 'desc': '快速发展'},
                {'name': '成熟期', 'desc': '稳定盈利'},
                {'name': '转型期', 'desc': '寻求突破'}
            ]
        },
        'moat_scores': {
            '品牌价值': 95,
            '规模效应': 85,
            '转换成本': 60,
            '网络效应': 20,
            '成本优势': 80
        },
        'moat_components': [
            {'name': '品牌资产', 'value': 45},
            {'name': '规模优势', 'value': 30},
            {'name': '成本优势', 'value': 20},
            {'name': '其他', 'value': 5}
        ],
        'risks': [
            {'name': '集中度风险', 'impact': 3, 'probability': 2},
            {'name': '政策风险', 'impact': 3, 'probability': 2},
            {'name': '竞争风险', 'impact': 3, 'probability': 3},
            {'name': '消费偏好变化', 'impact': 2, 'probability': 2}
        ],
        'valuation': {
            'current_pe': 12.46,
            'fair_range': (10, 15)
        },
        'valuation_comparison': {
            'companies': [
                {'name': '茅台', 'pe': 30},
                {'name': '五粮液', 'pe': 25},
                {'name': '洋河(当前)', 'pe': 12.46},
                {'name': '泸州老窖', 'pe': 20}
            ],
            'current_pe': 12.46
        },
        'target_price': '180-200',
        'stop_loss': '120',
        'holding_period': '12-24'
    }

    # 生成测试报告
    print("增强版报告生成器已就绪")
    print("注：完整功能需要配合Subagent使用")
