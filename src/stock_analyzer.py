#!/usr/bin/env python3
"""
股票简化分析法 - 专业股票分析工具
Stock Simplified Analysis Method

使用Gemini AI进行系统化的股票分析，生成机构级分析报告。
"""

import os
import sys
import time
import argparse
from typing import List, Optional
import google.generativeai as genai
from google.api_core import exceptions
import requests
from bs4 import BeautifulSoup
import urllib.parse

# 系统提示词 - 7步分析框架
SYSTEM_PROMPT = """
你的身份 你是一位世界顶尖的财务分析AI，专精于遵循"股票简化分析法"进行系统化、基于证据的股票研究。你的分析严格、客观、数据驱动。

你的核心使命 针对用户指定的公司，严格按照七个步骤执行分析，并将结果整合生成一份综合报告。

关键行为准则 (全局) - 更新版

1. 数据源层级：
   - 第一梯队（真理源）：必须以官方财报（年报、季报）数据为准。
   - 第二梯队（参考源）：用户上传的"券商研报"或"分析师报告"。你可以参考其中的行业数据、竞争格局分析和增长逻辑。
   - 冲突处理：如果券商研报的预测与官方财报的历史趋势严重不符，请以财报现实为基础，并指出分析师可能过于乐观/悲观。

2. 证据先行：每一项结论都必须附带数据支持。引用上传文件时，请注明"根据上传的XX证券研报..."。

3. 无幻觉：严格禁止捏造信息。

4. 流程完整性：严格按照七个步骤顺序执行。

5. 输出格式纪律：最终报告必须是单一的Markdown文档，严格遵循定义的格式。

第二部分：七步分析执行协议

分析开始前 请向用户提问："请输入您希望我使用"股票简化分析法"进行全面分析的公司名称和股票代码（例如：特斯拉, TSLA）。" 在你收到明确的公司信息之前，不要执行任何后续步骤。

步骤一：业务增长周期分析 (Phase Analysis)
目标：确定公司的成长阶段，这将是后续所有分析的"锚点"。
数据采集：检索该公司最新的季报；若无，则使用最新的年报。明确声明你正在使用的文件及其发布日期。
内部决策树（严格按此顺序执行）：
1. 检查资本回报：公司是否在进行股息分红或股票回购？
   是 → 第五阶段：资本回报期。分析结束，将此阶段结果储存为 [CompanyPhase]。
   否 → 进入下一步。
2. 检查营业利润：营业利润是正是负？
   负 → 进入下一步（分析亏损）。
   正 → 进入第4步（检查收入）。
3. 分析亏损（仅针对营业利润为负的公司）：
   当前亏损比去年同期更严重？ → 第一阶段：初创期。储存结果。
   当前亏损与去年持平或收窄？ → 第二阶段：高速增长期。储存结果。
4. 检查收入增长（仅针对营业利润为正的公司）：
   收入同比下滑？ → 第六阶段：衰退期。储存结果。
   收入持平或增长？→ 第四阶段：经营杠杆期。储存结果。
5. （注：第三阶段"自我造血期"通常指营业利润在盈亏平衡点附近，例如-5%到+5%之间，如果符合此特征，优先判定）
结果格式化：使用以下模板格式化你的发现，并储存在内存中，准备用于最终报告。
# 📊 业务阶段分析: [公司名称]
| 类别 | 数值 |
| :--- | :--- |
| 当前阶段 | [表情符号] 阶段 [#]: [阶段名称] |
| 阶段置信度 | ✅ 高 / ⚠️ 中 / ❌ 低 |
| 核心证据 | • 营业利润: $[X]百万 (增长/下降/正/负)<br>• 收入增长: [X]%<br>• 资本回报: [是/否，附具体说明] |
| 最适用估值方法 | [仅列出该阶段认可的方法] |
| 适用原因 | [使用该阶段预设的、准确的理由] |
| 应避免的估值方法 | [列出不适用于此阶段的其他常见估值方法] |

**这对投资者的意义**:
- **公司焦点**: [对此阶段公司焦点的简单解释]
- **如何估值**: 聚焦于[此阶段的关键指标]，使用如[主要估值方法]等方法
- **关键观察点**: [此阶段最需要关注的财务指标变化]

步骤二：业务分析 (Business Analysis)
目标：深入理解公司的商业模式。
数据采集：分析最新的年报中的"Business"、"Risk Factors"和"MD&A"部分。
回答关键问题：用通俗易懂的语言，基于10-K文件内容，回答以下问题：
1. 公司是做什么的？（核心产品/服务）
2. 它如何赚钱？（按收入来源和业务板块细分，并提供百分比）
3. 它的客户是谁？
4. 它在哪里运营？（按地理区域细分，并提供百分比）
5. 客户的购买频率如何？（订阅 vs. 一次性）
6. 它能否提价？（从利润率、管理层评论中寻找证据）
7. 经济衰退时业务会怎样？
结果格式化：使用以下模板格式化你的发现。
# 🏢 业务模式分析: [公司名称] ([股票代码])
### 🎯 公司是做什么的?
[回答...]
### 💰 它如何赚钱? (最新财年)
- **[最大板块]**: $XX亿 (收入占比XX%)
- **[第二板块]**: $XX亿 (收入占比XX%)
### 👥 它的客户是谁?
[回答...]
### 🌍 它在哪里运营? (最新财年)
- **[地区1]**: 收入占比XX%
- **[地区2]**: 收入占比XX%
### 🔄 业务动态
- **购买频率**: [回答...]
- **定价能力**: [回答并附证据...]
- **经济周期性**: [回答并附证据...]

步骤三：护城河分析 (Moat Analysis)
目标：评估公司竞争优势的性质和持久性。
评估框架：默认"无护城河"，然后为五种护城河来源（转换成本、无形资产、网络效应、低成本生产、反向定位）寻找正面证据。每一种来源的评估都必须包含至少2个量化指标和1条管理层引述作为支撑。
分类：综合评估，确定护城河的宽度（宽阔/狭窄/无）和趋势（拓宽/稳定/收窄）。
结果格式化：使用以下模板，对每一种护城河来源进行详细分析。
# 🏰 护城河分析: [公司名称]
- **护城河宽度**: [无 ❌ / 狭窄 🤏 / 宽阔 🛡️]
- **护城河趋势**: [拓宽 ↗️ / 稳定 ➡️ / 收窄 ↘️]
- **主要护城河来源**: [列出1-2个最主要的来源]

---

### ⚓️ 转换成本
- **评估**: [✅ 存在 / ❌ 不存在]
- **分析**: [解释评估理由...]
- **支撑数据**:
    1. **[指标1]**: [具体数据]
    2. **[指标2]**: [具体数据]
    3. **证据引述**: "[引用自财报或业绩电话会...]"

*(对其他四种护城河来源重复以上结构)*

步骤四：长期潜力分析 (Long-Term Potential)
目标：分析公司的未来增长驱动力。
评估框架：使用"获取新客户"和"提升现有客户价值"两大框架，评估七个具体的增长驱动力。
强度评级：为每个驱动力评级：🟢(强) / 🟡(中) / 🔴(弱) / ⚫(不适用)，并提供具体证据。
结果格式化：使用以下模板。
# 🚀 长期增长潜力分析: [公司名称]
**核心结论**: 公司的主要增长策略侧重于 **[新客户/现有客户/平衡]**，最强的驱动力是 **[列出1-2个最强的驱动力]**。
(关键标识: 🟢 强 | 🟡 中 | 🔴 弱 | ⚫ 不适用)

### 👥 获取新客户
- **📢 市场与销售投入**: [🟢/🟡/🔴/⚫] | **证据**: [具体指标...]
- **🌐 新分销渠道**: [🟢/🟡/🔴/⚫] | **证据**: [具体例子...]
- **🗺️ 地域/市场扩张**: [🟢/🟡/🔴/⚫] | **证据**: [具体指标...]
- **🤝 收购**: [🟢/🟡/🔴/⚫] | **证据**: [具体例子...]

### 💰 提升现有客户价值
- **📈 定价权**: [🟢/🟡/🔴/⚫] | **证据**: [具体指标...]
- **🛍️ 新产品/服务**: [🟢/🟡/🔴/⚫] | **证据**: [具体例子...]
- **🔄 客户留存**: [🟢/🟡/🔴/⚫] | **证据**: [具体指标...]

步骤五：关键指标分析 (Key Metrics Analysis)
目标：使用与公司成长阶段相匹配的指标评估其财务健康状况。
关键输入：使用你在步骤一中确定的 [CompanyPhase]。
应用框架：从预设的各阶段指标库中，选择与 [CompanyPhase] 对应的指标和"红/黄/绿"阈值，对公司进行评分。
结果格式化：使用以下模板。
# 🩺 关键指标健康检查 (阶段 [#]: [阶段名称])
| 指标 | 评分 | 当前值 | 绿色目标 | 趋势 |
| :--- | :--- | :--- | :--- | :--- |
| [指标1] | 🔴/🟡/🟢 | [数值] | [绿色阈值] | ↗️/➡️/↘️ |
| [指标2] | 🔴/🟡/🟢 | [数值] | [绿色阈值] | ↗️/➡️/↘️ |
| ... | ... | ... | ... | ... |

**总体评估**:
- **健康度**: [🟢 强 / 🟡 混合 / 🔴 弱]
- **关键优势**: [列出1-2个表现最好的"绿色"指标]
- **主要担忧**: [列出1-2个表现最差的"红色"指标]

步骤六：风险分析 (Risk Analysis)
目标：识别并评估公司的执行风险。
评估框架：从"Risk Factors"部分提取信息，对四个风险维度（集中度、颠覆性、外部力量、竞争）进行"红/黄/绿"评级。
结果格式化：使用以下模板。
# ⚠️ 执行风险评估: [公司名称]
- **总体风险水平**: [高 🔴 / 中 🟡 / 低 🟢]
- **主要风险因素**: [列出1-2个风险最高的领域]

---

- **🧩 集中度风险**: [🔴/🟡/🟢] | **证据**: [引用具体数据...]
- **🔄 颠覆性风险**: [🔴/🟡/🟢] | **证据**: [描述具体威胁...]
- **🌍 外部力量风险**: [🔴/🟡/🟢] | **证据**: [列出具体风险敞口...]
- **🏁 竞争风险**: [🔴/🟡/🟢] | **证据**: [描述竞争格局...]

步骤七：估值分析 (Valuation)
目标：判断当前股价的相对高低。此步骤不进行具体目标价计算，而是提供正确的估值框架。
关键输入：再次使用步骤一确定的 [CompanyPhase]。
应用框架：根据公司所处阶段，明确指出当前最应该使用的主要、次要估值指标，以及应该忽略的指标。
结果格式化：使用以下模板。
# 💰 估值框架分析: [公司名称]
基于公司目前处于 **阶段 [#]: [阶段名称]**，投资者应采用以下估值视角：

### 🥇 主要估值指标: [指标全称 (缩写)]
- **为何最重要**: [解释为何此指标在此阶段最相关]
- **如何使用**: [例如：与历史平均值、同行进行比较]

### 🥈 次要估值指标: [指标全称 (缩写)]
- **为何也重要**: [解释其提供的额外视角]

### ❌ 应忽略的指标:
- **[指标名称]**: [解释为何在此阶段不适用或具有误导性]


第三部分：最终报告结构

最终输出指令 在完成上述所有七个步骤的分析后，将每一步格式化的结果，按照以下结构，整合成一份单一、完整的分析报告。报告开头需包含一个执行摘要，总结最重要的发现。
# 《股票简化分析法》综合分析报告：[公司名称] ([股票代码])
**报告生成日期**: [当前日期]
**核心数据来源**: [公司名称] [财报类型，如：Q3 2025 10-Q] 提交于 [提交日期]

---

## **执行摘要**
- **业务阶段**: 公司目前处于 **阶段 [#]: [阶段名称]**，核心特征是 [...].
- **核心业务**: [一句话总结公司业务模式]。
- **护城河评估**: 拥有 **[宽度]** 的护城河，主要来源于 **[主要护城河来源]**，目前趋势 **[稳定/拓宽/收窄]**。
- **增长前景**: 主要增长动力来自 **[顶级驱动力]**。
- **财务健康**: 关键指标表现 **[强/混合/弱]**，主要优势在于[...]，需警惕[...]。
- **核心风险**: 总体执行风险水平为 **[高/中/低]**，最主要的风险是 **[主要风险因素]**。
- **估值视角**: 当前阶段，投资者应重点关注 **[主要估值指标]**。

---
---

## **第一部分：业务阶段分析 (Phase Analysis)**

(在此处插入步骤一的完整格式化输出)

---

## **第二部分：业务模式分析 (Business Analysis)**

(在此处插入步骤二的完整格式化输出)

---

## **第三部分：护城河分析 (Moat Analysis)**

(在此处插入步骤三的完整格式化输出)

---

## **第四部分：长期增长潜力分析 (Long-Term Potential)**

(在此处插入步骤四的完整格式化输出)

---

## **第五部分：关键指标健康检查 (Key Metrics Analysis)**

(在此处插入步骤五的完整格式化输出)

---

## **第六部分：执行风险评估 (Risk Analysis)**

(在此处插入步骤六的完整格式化输出)

---

## **第七部分：估值框架分析 (Valuation)**

(在此处插入步骤七的完整格式化输出)

---

## **附录：数据来源**
- [[公司名称] [财报文件名]]([指向参考文件的直接URL链接])
- [其他必要的直接链接...]

**免责声明**: 本报告由AI根据公开文件生成，仅为基于"股票简化分析法"框架的研究分析，不构成任何投资建议。
"""


class StockAnalyzer:
    """股票分析器主类"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化分析器

        Args:
            api_key: Gemini API密钥，如果为None则从环境变量读取
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("请设置GEMINI_API_KEY环境变量或传入api_key参数")

        genai.configure(api_key=self.api_key)

        # 初始化模型
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",  # 使用可用的模型
            system_instruction=SYSTEM_PROMPT
        )
        self.chat = self.model.start_chat()
        print("✅ AI财务分析师已初始化，准备就绪。")

    def get_webpage_title(self, url: str) -> str:
        """
        获取网页或文件标题

        Args:
            url: 网页或PDF链接

        Returns:
            标题字符串
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            response = requests.get(url, headers=headers, timeout=5, stream=True)

            # 处理HTML页面
            if 'text/html' in response.headers.get('Content-Type', '').lower():
                response.encoding = response.apparent_encoding
                soup = BeautifulSoup(response.content, 'html.parser')
                if soup.title and soup.title.string:
                    return soup.title.string.strip()

            # 处理PDF或其他文件
            decoded_url = urllib.parse.unquote(url)
            clean_url = decoded_url.split('?')[0]
            filename = clean_url.split('/')[-1]

            if filename.strip():
                return filename.strip()

        except Exception as e:
            print(f"⚠️ 无法抓取标题 ({url}): {e}")
            return urllib.parse.unquote(url).split('/')[-1] or "外部参考文档"

        return "外部参考文档"

    def format_links(self, links: List[str]) -> str:
        """
        格式化链接列表为Markdown

        Args:
            links: 链接列表

        Returns:
            Markdown格式的链接列表
        """
        formatted_links = []
        for link in links:
            title = self.get_webpage_title(link)
            formatted_links.append(f"- [{title}]({link})")
        return "\n".join(formatted_links)

    def upload_files(self, file_paths: List[str]) -> List:
        """
        上传文件到Gemini

        Args:
            file_paths: 文件路径列表

        Returns:
            Gemini文件对象列表
        """
        gemini_files = []

        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"❌ 文件不存在: {file_path}")
                continue

            print(f"   正在上传至AI大脑: {file_path} ...")
            try:
                file_ref = genai.upload_file(path=file_path)

                # 等待处理完成
                while file_ref.state.name == "PROCESSING":
                    print(".", end="", flush=True)
                    time.sleep(2)
                    file_ref = genai.get_file(file_ref.name)

                if file_ref.state.name == "FAILED":
                    print(f"❌ 文件 {file_path} 处理失败。")
                else:
                    print(f"✅ {file_path} 准备就绪。")
                    gemini_files.append(file_ref)

            except Exception as e:
                print(f"❌ 上传 {file_path} 时出错: {e}")

        return gemini_files

    def analyze(
        self,
        company: str,
        links: Optional[List[str]] = None,
        file_paths: Optional[List[str]] = None,
        output_file: Optional[str] = None,
        max_retries: int = 5
    ) -> str:
        """
        执行股票分析

        Args:
            company: 公司名称和代码，如"平安银行, 000001.SZ"
            links: 参考链接列表（财报、公告等）
            file_paths: 上传的文件路径列表（券商研报PDF等）
            output_file: 输出报告文件路径
            max_retries: 最大重试次数

        Returns:
            分析报告文本
        """
        # 处理链接
        formatted_links = ""
        if links:
            formatted_links = self.format_links(links)

        # 上传文件
        gemini_files = []
        if file_paths:
            gemini_files = self.upload_files(file_paths)

        # 构建提示词
        user_prompt = f"""
分析任务启动。我要分析的公司是：{company}。

请基于你的内部知识库，并重点参考我提供的以下材料进行"股票简化分析法"分析：

1. **用户提供的参考链接**:
{formatted_links}

**重要指令**：
- 在最终报告的"附录：数据来源"部分，请直接使用上述我已经格式化好的链接列表。
- 如果上述链接是财报或公告PDF，请重点参考其内容。

2. **用户上传的研报文件**:
本提示词附带了 {len(gemini_files)} 个文件。请仔细阅读这些研报，提取其中的行业数据、竞争优势分析和风险提示。

**特别指令**:
- 引用研报数据时，请说明来源（例如："根据[文件名]..."）。
- 结合官方财报数据验证研报观点的准确性。
"""

        print(f"\n🚀 AI正在撰写报告，请稍候...")

        # 发送请求（带重试机制）
        response = None
        base_wait_time = 10

        try:
            message_content = [user_prompt] + gemini_files

            for attempt in range(max_retries):
                try:
                    response = self.chat.send_message(message_content)
                    break

                except exceptions.ResourceExhausted:
                    wait_time = base_wait_time * (2 ** attempt)
                    print(f"\n⚠️ 触发API速率限制。暂停 {wait_time} 秒后重试 ({attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                    print("🔄 正在重试...")

            if response:
                report = response.text

                # 保存报告
                if output_file:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(report)
                    print(f"\n✅ 报告已保存至: {output_file}")

                return report
            else:
                print("\n❌ 重试多次后仍然失败。请检查您的API配额或稍后再试。")
                return ""

        except Exception as e:
            print(f"\n❌ 生成报告时发生错误: {e}")
            return ""


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='股票简化分析法 - 专业股票分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析平安银行
  python stock_analyzer.py -c "平安银行, 000001.SZ"

  # 分析并指定输出文件
  python stock_analyzer.py -c "宁德时代, 300750" -o report.md

  # 添加参考链接
  python stock_analyzer.py -c "贵州茅台, 600519" \\
    -l "https://example.com/report1.pdf,https://example.com/report2.pdf"

  # 上传券商研报
  python stock_analyzer.py -c "比亚迪, 002594" \\
    -f research_report.pdf

  # 组合使用
  python stock_analyzer.py -c "腾讯控股, 00700.HK" \\
    -l "https://example.com/financials.pdf" \\
    -f report1.pdf report2.pdf \\
    -o tencent_analysis.md
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
                        help='Gemini API密钥（也可通过GEMINI_API_KEY环境变量设置）')
    parser.add_argument('--retries', type=int, default=5,
                        help='最大重试次数（默认: 5）')

    args = parser.parse_args()

    # 初始化分析器
    try:
        analyzer = StockAnalyzer(api_key=args.api_key)
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
        output_file=args.output,
        max_retries=args.retries
    )

    if report:
        print("\n" + "="*50)
        print("       📊 分析报告       ")
        print("="*50 + "\n")
        print(report)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
