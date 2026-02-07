
summary_prompt = """
你是报告整合专家。请根据以下7个分析步骤的结果，生成一份综合的执行摘要。

公司：{company}

各步骤分析结果：
1. 业务阶段：{phase_result}
2. 业务模式：{business_result}
3. 护城河：{moat_result}
4. 增长潜力：{growth_result}
5. 关键指标：{metrics_result}
6. 风险评估：{risk_result}
7. 估值框架：{valuation_result}

请生成一份简洁的执行摘要，包含以下要点：
- 业务阶段
- 核心业务
- 护城河评估
- 增长前景
- 财务健康
- 核心风险
- 估值视角

格式要求：
- 使用简洁的要点列表
- 每个要点1-2句话
- 保持客观专业
"""
