#!/usr/bin/env python3
"""
Stock Subagent System
股票分析Subagent系统 - 将7步分析法拆分为7个专业化subagent
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

# 添加项目路径
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_DIR, 'src'))

from google import genai
from google.genai import types

# 导入 Prompts
from analysis_prompts import (
    phase_analysis,
    business_analysis,
    moat_analysis,
    growth_analysis,
    metrics_analysis,
    risk_analysis,
    valuation_analysis,
    summary_report
)


from chart_generator import StockChartGenerator
from html_report_generator import HtmlReportGenerator


class StockSubagent:
    """股票分析Subagent基类"""

    def __init__(self, api_key: str, model: str = 'gemini-2.5-flash'):
        """初始化subagent"""
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.agent_name = self.__class__.__name__

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行分析

        Args:
            context: 包含公司信息、Tushare数据、PDF内容等的上下文

        Returns:
            分析结果字典
        """
        raise NotImplementedError("子类必须实现此方法")

    def call_gemini(self, prompt: str, system_prompt: str = "") -> str:
        """调用Gemini API"""
        try:
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    top_p=0.9,
                )
            )

            if response and response.text:
                return response.text
            else:
                return "分析失败：未返回结果"

        except Exception as e:
            return f"分析失败：{str(e)}"


class PhaseAnalysisSubagent(StockSubagent):
    """步骤1: 业务增长周期分析"""

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        company = context.get('company', '')
        tushare_data = context.get('tushare_data', '')
        pdf_content = context.get('pdf_content', '')

        # 构建数据部分
        data_sources = []
        if pdf_content:
            data_sources.append(f"PDF内容: {pdf_content}")
        else:
            data_sources.append('未上传PDF文件')

        if tushare_data:
            data_sources.append(f"Tushare MCP 数据：\n{tushare_data}")
        else:
            data_sources.append('无Tushare数据')

        # 使用模板构建 prompt
        system_prompt = phase_analysis.system_prompt
        prompt = phase_analysis.user_prompt.format(
            company=company,
            data_sources=chr(10).join(data_sources)
        )

        result = self.call_gemini(prompt, system_prompt)

        return {
            'step': 1,
            'name': '业务阶段分析',
            'result': result,
            'status': 'completed'
        }


class BusinessAnalysisSubagent(StockSubagent):
    """步骤2: 业务分析"""

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        company = context.get('company', '')
        tushare_data = context.get('tushare_data', '')
        pdf_content = context.get('pdf_content', '')

        # 构建数据部分
        data_sources = []
        if pdf_content:
            data_sources.append(f"PDF内容: {pdf_content}")
        else:
            data_sources.append('未上传PDF文件')

        if tushare_data:
            data_sources.append(f"Tushare MCP 数据：\n{tushare_data}")
        else:
            data_sources.append('无Tushare数据')

        # 使用模板构建 prompt
        system_prompt = business_analysis.system_prompt
        prompt = business_analysis.user_prompt.format(
            company=company,
            data_sources=chr(10).join(data_sources)
        )

        result = self.call_gemini(prompt, system_prompt)

        return {
            'step': 2,
            'name': '业务模式分析',
            'result': result,
            'status': 'completed'
        }


class MoatAnalysisSubagent(StockSubagent):
    """步骤3: 护城河分析"""

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        company = context.get('company', '')
        phase_result = context.get('phase_result', '')
        business_result = context.get('business_result', '')
        tushare_data = context.get('tushare_data', '')
        pdf_content = context.get('pdf_content', '')

        # 使用模板构建 prompt
        system_prompt = moat_analysis.system_prompt
        prompt = moat_analysis.user_prompt.format(
            company=company,
            phase_result=phase_result[:500] if phase_result else '未完成',
            business_result=business_result[:500] if business_result else '未完成',
            tushare_data=tushare_data[:500] if tushare_data else '无',
            pdf_content=pdf_content[:500] if pdf_content else '无'
        )

        result = self.call_gemini(prompt, system_prompt)

        return {
            'step': 3,
            'name': '护城河分析',
            'result': result,
            'status': 'completed'
        }


class GrowthPotentialSubagent(StockSubagent):
    """步骤4: 长期增长潜力分析"""

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        company = context.get('company', '')
        business_result = context.get('business_result', '')
        tushare_data = context.get('tushare_data', '')
        pdf_content = context.get('pdf_content', '')

        # 使用模板构建 prompt
        system_prompt = growth_analysis.system_prompt
        prompt = growth_analysis.user_prompt.format(
            company=company,
            business_result=business_result[:500] if business_result else '未完成',
            tushare_data=tushare_data[:500] if tushare_data else '无',
            pdf_content=pdf_content[:500] if pdf_content else '无'
        )

        result = self.call_gemini(prompt, system_prompt)

        return {
            'step': 4,
            'name': '长期增长潜力分析',
            'result': result,
            'status': 'completed'
        }


class KeyMetricsSubagent(StockSubagent):
    """步骤5: 关键指标分析"""

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        company = context.get('company', '')
        phase_result = context.get('phase_result', '')
        tushare_data = context.get('tushare_data', '')
        pdf_content = context.get('pdf_content', '')

        # 使用模板构建 prompt
        system_prompt = metrics_analysis.system_prompt
        prompt = metrics_analysis.user_prompt.format(
            company=company,
            phase_result=phase_result[:300] if phase_result else '未完成',
            tushare_data=tushare_data if tushare_data else '无'
        )

        result = self.call_gemini(prompt, system_prompt)

        return {
            'step': 5,
            'name': '关键指标健康检查',
            'result': result,
            'status': 'completed'
        }


class RiskAnalysisSubagent(StockSubagent):
    """步骤6: 风险分析"""

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        company = context.get('company', '')
        business_result = context.get('business_result', '')
        moat_result = context.get('moat_result', '')
        tushare_data = context.get('tushare_data', '')
        pdf_content = context.get('pdf_content', '')

        # 使用模板构建 prompt
        system_prompt = risk_analysis.system_prompt
        prompt = risk_analysis.user_prompt.format(
            company=company,
            business_result=business_result[:300] if business_result else '未完成',
            moat_result=moat_result[:300] if moat_result else '未完成',
            tushare_data=tushare_data[:500] if tushare_data else '无',
            pdf_content=pdf_content[:500] if pdf_content else '无'
        )

        result = self.call_gemini(prompt, system_prompt)

        return {
            'step': 6,
            'name': '执行风险评估',
            'result': result,
            'status': 'completed'
        }


class ValuationSubagent(StockSubagent):
    """步骤7: 估值分析"""

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        company = context.get('company', '')
        phase_result = context.get('phase_result', '')
        tushare_data = context.get('tushare_data', '')
        pdf_content = context.get('pdf_content', '')

        # 使用模板构建 prompt
        system_prompt = valuation_analysis.system_prompt
        prompt = valuation_analysis.user_prompt.format(
            company=company,
            phase_result=phase_result[:300] if phase_result else '未完成',
            tushare_data=tushare_data if tushare_data else '无'
        )

        result = self.call_gemini(prompt, system_prompt)

        return {
            'step': 7,
            'name': '估值框架分析',
            'result': result,
            'status': 'completed'
        }


class SubagentOrchestrator:
    """Subagent协调器 - 管理整个分析流程"""

    def __init__(self, api_key: str):
        """初始化协调器"""
        self.api_key = api_key
        self.subagents = {
            'phase': PhaseAnalysisSubagent(api_key),
            'business': BusinessAnalysisSubagent(api_key),
            'moat': MoatAnalysisSubagent(api_key),
            'growth': GrowthPotentialSubagent(api_key),
            'metrics': KeyMetricsSubagent(api_key),
            'risk': RiskAnalysisSubagent(api_key),
            'valuation': ValuationSubagent(api_key),
        }
        self.chart_generator = StockChartGenerator()
        self.html_generator = HtmlReportGenerator()

    def _extract_chart_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        从分析结果中提取图表数据
        通过调用 Gemini 将非结构化文本转换为 JSON
        """
        print("📊 正在提取图表数据...")
        
        # 准备输入文本
        summary_text = ""
        for key, val in results.items():
            summary_text += f"\n=== {val['name']} ===\n{val['result']}\n"
            
        prompt = """
        请从以上股票分析报告中提取关键数据，用于生成图表。
        请严格返回合法的 JSON 格式，不要包含 Markdown 代码块标记。
        
        需要提取的数据结构如下：
        {
            "radar_scores": {
                "business": 0-100,  // 业务模式评分
                "moat": 0-100,      // 护城河评分
                "financial": 0-100, // 财务健康评分
                "growth": 0-100,    // 增长潜力评分
                "safety": 0-100     // 安全性(100-风险)评分
            },
            "moat_scores": {        // 各护城河维度得分 (0-5)
                "switching_costs": 0-5,
                "intangible_assets": 0-5,
                "network_effect": 0-5,
                "cost_advantage": 0-5,
                "efficient_scale": 0-5
            },
            "financial_health": {   // 财务指标状态 (1=差, 2=中, 3=好)
                "profitability": 1-3,
                "solvency": 1-3,
                "growth": 1-3,
                "efficiency": 1-3
            },
            "valuation": {
                "current_price": 0.0,   // 如果提到
                "fair_value_min": 0.0,  // 估值下限
                "fair_value_max": 0.0,  // 估值上限
                "status": "undervalued/fair/overvalued" // 状态
            }
        }
        
        如果某些数据未明确提及，请根据上下文进行合理估算。
        """
        
        client = genai.Client(api_key=self.api_key)
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"{summary_text}\n\n{prompt}",
                config=types.GenerateContentConfig(temperature=0.1, response_mime_type="application/json")
            )
            
            if response and response.text:
                import json
                # 清理可能的 markdown 标记
                text = response.text.replace('```json', '').replace('```', '').strip()
                return json.loads(text)
        except Exception as e:
            print(f"⚠️ 数据提取失败: {e}")
            
        # 返回默认数据以防失败
        return {
            "radar_scores": {"business": 60, "moat": 50, "financial": 60, "growth": 60, "safety": 60},
            "moat_scores": {"switching_costs": 3, "intangible_assets": 3, "network_effect": 2, "cost_advantage": 3, "efficient_scale": 2},
            "financial_health": {"profitability": 2, "solvency": 2, "growth": 2, "efficiency": 2},
            "valuation": {"status": "fair"}
        }

    def _generate_charts(self, data: Dict[str, Any]) -> Dict[str, str]:
        """生成图表并返回路径字典"""
        print("🎨 正在生成专业图表...")
        chart_paths = {}
        
        try:
            # 1. 投资雷达图
            radar = data.get('radar_scores', {})
            path = self.chart_generator.create_investment_radar(
                scores_dict={
                    '业务阶段': radar.get('business', 60),
                    '护城河': radar.get('moat', 50),
                    '财务健康': radar.get('financial', 60),
                    '增长潜力': radar.get('growth', 60),
                    '风险控制': radar.get('safety', 60)
                }
            )
            chart_paths['CHART_RADAR'] = path
            
            # 2. 护城河评分图
            moat = data.get('moat_scores', {})
            # 转换 0-5 为 0-100
            path = self.chart_generator.create_moat_radar(
                moat_scores={
                    '转换成本': moat.get('switching_costs', 3) * 20,
                    '无形资产': moat.get('intangible_assets', 3) * 20,
                    '网络效应': moat.get('network_effect', 2) * 20,
                    '成本优势': moat.get('cost_advantage', 3) * 20,
                    '规模效应': moat.get('efficient_scale', 2) * 20
                },
                save_path=self.chart_generator.output_dir / 'moat_radar.png'
            )
            chart_paths['CHART_MOAT'] = path
            
            # 3. 财务热力图
            fin = data.get('financial_health', {})
            # 转换 1-3 为 0-100
            path = self.chart_generator.create_financial_heatmap(
                heatmap_data={
                    '盈利能力': [fin.get('profitability', 2) * 33],
                    '偿债能力': [fin.get('solvency', 2) * 33],
                    '成长能力': [fin.get('growth', 2) * 33],
                    '运营效率': [fin.get('efficiency', 2) * 33]
                }
            )
            chart_paths['CHART_FINANCIAL'] = path
            
            # 4. 估值正态分布
            val = data.get('valuation', {})
            status = val.get('status', 'fair')
            current_pe = 20 # 默认
            fair_min = 15
            fair_max = 25
            
            if status == 'undervalued': 
                current_pe = 12
            elif status == 'overvalued': 
                current_pe = 30
            
            path = self.chart_generator.create_valuation_bell_curve(
                current_pe=current_pe,
                fair_range=(fair_min, fair_max)
            )
            chart_paths['CHART_VALUATION'] = path
            
        except Exception as e:
            print(f"⚠️ 图表生成部分失败: {e}")
            
        return chart_paths

    def run(self, company: str, ts_code: Optional[str] = None, pdf_content: str = '') -> str:
        """
        执行完整流程：获取数据 -> 分析 -> 提取数据 -> 绘图 -> 生成HTML报告
        """
        # 1. 获取 Tushare 数据
        tushare_data = ""
        if ts_code:
            try:
                from tushare_mcp_client import get_tushare_client
                client = get_tushare_client()
                if client:
                    print(f"📊 正在获取 {ts_code} 的实时数据...")
                    tushare_data = client.get_all_data(ts_code)
                    print("✅ Tushare 数据获取完成")
            except Exception as e:
                print(f"⚠️ 获取 Tushare 数据失败: {e}")

        # 2. 运行分析
        results = self.run_analysis(company, tushare_data, pdf_content)

        # 3. 提取数据并绘图
        chart_data = self._extract_chart_data(results)
        chart_paths = self._generate_charts(chart_data)

        # 4. 生成 Markdown 报告
        print("📝 正在生成最终综合报告...")
        markdown_report = self.generate_final_report(company, results)
        
        # 5. 生成 HTML 报告 (默认输出)
        # 确定输出文件名
        timestamp = datetime.now().strftime('%Y%m%d')
        safe_name = company.split(',')[0].strip().replace(' ', '_')
        output_file = f"{safe_name}_分析报告_{timestamp}.html"
        
        self.html_generator.generate_report(
            markdown_content=markdown_report,
            chart_paths=chart_paths,
            output_path=output_file
        )

        return output_file

    def run_analysis(self, company: str, tushare_data: str = '',
                     pdf_content: str = '') -> Dict[str, Any]:
        """
        运行完整的7步分析

        Args:
            company: 公司名称和代码
            tushare_data: Tushare数据
            pdf_content: PDF文件内容

        Returns:
            所有步骤的分析结果
        """
        # 构建共享上下文
        context = {
            'company': company,
            'tushare_data': tushare_data,
            'pdf_content': pdf_content,
        }

        # 执行顺序（基于依赖关系）
        execution_order = [
            ('phase', 'phase'),          # 步骤1：独立
            ('business', 'business'),    # 步骤2：独立
            ('moat', 'moat'),            # 步骤3：依赖1,2
            ('growth', 'growth'),        # 步骤4：依赖1,2
            ('metrics', 'metrics'),      # 步骤5：依赖1
            ('risk', 'risk'),            # 步骤6：依赖1,2,3
            ('valuation', 'valuation'),  # 步骤7：依赖所有
        ]

        results = {}
        print("\n" + "="*60)
        print("🚀 启动7步Subagent分析流程")
        print("="*60 + "\n")

        for step_key, agent_key in execution_order:
            print(f"📊 执行步骤 {results.get('phase', {}).get('step', 1)}: {self.subagents[agent_key].agent_name}")

            # 更新上下文（传递前面的结果）
            for prev_key, prev_result in results.items():
                context[f"{prev_key}_result"] = prev_result.get('result', '')

            # 执行分析
            result = self.subagents[agent_key].analyze(context)
            results[step_key] = result

            print(f"✅ {result['name']} 完成\n")

        print("="*60)
        print("✅ 所有分析步骤完成")
        print("="*60 + "\n")

        return results

    def generate_final_report(self, company: str, results: Dict[str, Any]) -> str:
        """生成最终报告"""
        # 提取各步骤结果
        phase_result = results['phase']['result']
        business_result = results['business']['result']
        moat_result = results['moat']['result']
        growth_result = results['growth']['result']
        metrics_result = results['metrics']['result']
        risk_result = results['risk']['result']
        valuation_result = results['valuation']['result']

        # 生成执行摘要
        summary_prompt = summary_report.summary_prompt.format(
            company=company,
            phase_result=phase_result[:300],
            business_result=business_result[:300],
            moat_result=moat_result[:300],
            growth_result=growth_result[:300],
            metrics_result=metrics_result[:300],
            risk_result=risk_result[:300],
            valuation_result=valuation_result[:300]
        )

        summary = "摘要生成失败"
        try:
            summary_client = genai.Client(api_key=self.api_key)
            summary_response = summary_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=summary_prompt,
                config=types.GenerateContentConfig(temperature=0.7)
            )
            summary = summary_response.text if summary_response.text else summary
        except Exception as e:
            print(f"⚠️ 摘要生成失败（离线模式）: {e}")
            # 离线兜底：拼接关键段落的前几句
            def _head(text: str, limit: int = 120) -> str:
                if not text:
                    return "（无内容）"
                t = text.strip().replace("\n", " ")
                return t[:limit] + ("…" if len(t) > limit else "")

            summary = "\n".join([
                f"1. 业务阶段：{_head(phase_result)}",
                f"2. 业务模式：{_head(business_result)}",
                f"3. 护城河：{_head(moat_result)}",
                f"4. 增长潜力：{_head(growth_result)}",
                f"5. 关键指标：{_head(metrics_result)}",
                f"6. 风险评估：{_head(risk_result)}",
                f"7. 估值分析：{_head(valuation_result)}",
            ])

        # 组装完整报告 (插入图表占位符)
        report = f"""
# 《股票简化分析法》综合分析报告：{company.split(',')[0].strip()}
**报告生成日期**: {datetime.now().strftime('%Y年%m月%d日')}
**分析方法**: Subagent架构（7个专业化分析agent）

---

## **执行摘要**
{summary}

### 投资分析雷达图
{{{{CHART_RADAR}}}}

---
---

## **第一部分：业务阶段分析 (Phase Analysis)**
{phase_result}

---

## **第二部分：业务模式分析 (Business Analysis)**
{business_result}

---

## **第三部分：护城河分析 (Moat Analysis)**
{moat_result}

### 护城河强度评分
{{{{CHART_MOAT}}}}

---

## **第四部分：长期增长潜力分析 (Long-Term Potential)**
{growth_result}

---

## **第五部分：关键指标健康检查 (Key Metrics Analysis)**
{metrics_result}

### 财务健康热力图
{{{{CHART_FINANCIAL}}}}

---

## **第六部分：执行风险评估 (Risk Analysis)**
{risk_result}

---

## **第七部分：估值框架分析 (Valuation)**
{valuation_result}

### 估值区间定位
{{{{CHART_VALUATION}}}}

---

**免责声明**: 本报告由AI Subagent系统根据公开文件生成，仅为基于"股票简化分析法"框架的研究分析，不构成任何投资建议。
"""

        return report


# 导出
__all__ = [
    'SubagentOrchestrator',
    'PhaseAnalysisSubagent',
    'BusinessAnalysisSubagent',
    'MoatAnalysisSubagent',
    'GrowthPotentialSubagent',
    'KeyMetricsSubagent',
    'RiskAnalysisSubagent',
    'ValuationSubagent',
]
