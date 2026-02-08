# 📊 股票简化分析法 (Stock Simplified Analysis Method)

[![Version](https://img.shields.io/badge/version-v2.1.0-blue.svg)](https://github.com/yanglaiyang/stock-analysis-skill/releases/tag/v2.1.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Tests](https://img.shields.io/badge/tests-7%2F7%20passing-success.svg)](src/test_chart_optimization.py)

一个专业、系统化的股票分析工具，使用AI执行"股票简化分析法"七步分析框架，生成机构级股票分析报告，支持15种专业可视化图表，并支持复杂HTML图表结构与Mermaid渲染。新版本已**符合 Claude Code Skill 规范**。

## ✨ 特性

- 🎯 **七步系统化分析**: 从业务阶段到估值的完整分析框架
- 🤖 **AI驱动**: 基于Gemini AI的智能分析能力
- 🔗 **Tushare MCP支持**: 可接入实时/结构化数据源
- 🧠 **Subagent架构**: 7个专业化分析Agent协作完成全流程分析
- 📊 **15种专业图表**: 雷达图、矩阵图、热力图等可视化
- 🌏 **完美中文支持**: 自动检测字体，跨平台兼容
- 🖥️ **无GUI环境支持**: 可在服务器/Docker环境中运行
- 📄 **多格式支持**: 支持PDF、HTML、URL等多种数据源
- 🔄 **自动重试**: 内置API限流处理机制
- 📝 **Markdown报告**: 生成格式精美的分析报告
- 🧩 **复杂HTML图表**: 支持多图表布局、Mermaid流程/决策树渲染
- ✅ **完整测试**: 7/7测试通过，代码质量保证

## 🔍 分析框架

本工具基于"股票简化分析法"，包含七个分析步骤：

1. **业务增长周期分析** - 确定公司所处的发展阶段
2. **业务分析** - 深入理解商业模式
3. **护城河分析** - 评估竞争优势
4. **长期潜力分析** - 分析增长驱动力
5. **关键指标分析** - 评估财务健康状况
6. **风险分析** - 识别执行风险
7. **估值分析** - 提供估值框架

## 📦 安装

### 环境要求

- Python 3.9 或更高版本
- Gemini API密钥（从 [Google AI Studio](https://aistudio.google.com/) 获取）

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yanglaiyang/stock-analysis-skill.git
cd stock-analysis-skill
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 设置API密钥

**Linux/Mac:**
```bash
export GEMINI_API_KEY='your_api_key_here'
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY='your_api_key_here'
```

或使用 `--api-key` 参数直接传入。

## 🚀 使用方法

### 作为 Claude Skill 使用

本项目包含 Claude Skill 规范文件：

- `.claude/skills/stock-analysis/SKILL.md`
- `.claude/skills/stock-analysis/reference.md`
- `.claude/skills/stock-analysis/examples.md`

当作为 Skill 使用时，直接按以下格式调用：

```text
股票分析：公司名, 代码
```

示例：

```text
股票分析：新华人寿, 601336.SH
```

> 注意：完整在线分析需要环境变量 `GEMINI_API_KEY` 或 `GOOGLE_API_KEY`。

### 基本用法

分析一只股票：

```bash
python src/stock_analyzer.py -c "平安银行, 000001.SZ"
```

### 保存报告

```bash
python src/stock_analyzer.py -c "宁德时代, 300750" -o report.md
```

### 添加参考链接

```bash
python src/stock_analyzer.py -c "贵州茅台, 600519" \
  -l "https://example.com/report1.pdf,https://example.com/report2.pdf"
```

### 上传券商研报

```bash
python src/stock_analyzer.py -c "比亚迪, 002594" -f research_report.pdf
```

### 组合使用

```bash
python src/stock_analyzer.py -c "腾讯控股, 00700.HK" \
  -l "https://example.com/financials.pdf" \
  -f report1.pdf report2.pdf \
  -o tencent_analysis.md \
  --retries 3
```

### 命令行参数

| 参数 | 简写 | 说明 | 必需 |
|------|------|------|------|
| --company | -c | 公司名称和代码 | ✅ |
| --links | -l | 参考链接（逗号分隔） | ❌ |
| --files | -f | 上传的文件路径 | ❌ |
| --output | -o | 输出报告文件路径 | ❌ |
| --api-key | -k | Gemini API密钥 | ❌ |
| --retries | - | 最大重试次数 | ❌ |

## 📝 报告示例

生成的报告包含以下部分：

- **执行摘要** - 快速了解核心发现
- **业务阶段分析** - 判断公司发展阶段
- **业务模式分析** - 深入了解商业模式
- **护城河分析** - 评估竞争优势
- **长期增长潜力** - 分析增长驱动力
- **关键指标健康检查** - 财务健康度评估
- **执行风险评估** - 识别主要风险
- **估值框架分析** - 提供估值视角
- **数据来源附录** - 完整的数据来源

## 🛠️ 开发

### 项目结构

```
stock-analysis-skill/
├── src/
│   ├── stock_analyzer.py        # 主程序
│   ├── chart_generator.py       # 图表生成器（已优化）
│   ├── font_config.py           # 字体配置模块（新增）
│   ├── chart_generator_v2.py    # 图表增强补丁（新增）
│   └── test_chart_optimization.py # 测试脚本（新增）
├── tests/
│   └── test_analyzer.py         # 单元测试
├── docs/
│   └── analysis_framework.md    # 分析框架文档
├── requirements.txt             # 依赖列表
├── README.md                    # 本文件
├── CHART_OPTIMIZATION_SUMMARY.md # 图表优化说明（新增）
└── skill.json                   # Skill配置文件
```

### 运行测试

**图表优化测试**:
```bash
python src/test_chart_optimization.py
```

**单元测试**:
```bash
python tests/test_analyzer.py
```

## 📊 图表系统

### 支持的图表类型

本工具支持 15 种专业可视化图表：

| 图表类型 | 说明 | 状态 |
|---------|------|------|
| 投资评分雷达图 | 五维评分可视化 | ✅ |
| 核心财务指标卡片 | 关键财务数据展示 | ✅ |
| 业务阶段时间轴 | 公司发展阶段 | ✅ |
| 商业画布图 | 商业模式分析 | ✅ |
| 产品矩阵象限图 | 产品组合分析 | ✅ |
| 护城河雷达图 | 竞争优势评估 | ✅ |
| 护城河瀑布图 | 护城河构成分析 | ✅ |
| 财务指标热力图 | 财务健康度热力图 | ✅ |
| 杜邦分析树状图 | ROE拆解分析 | ✅ |
| 现金流桑基图 | 现金流分析 | ✅ |
| 增长驱动力树状图 | 增长因素分析 | ✅ |
| 增长阶段曲线 | 增长轨迹分析 | ✅ |
| 风险矩阵图 | 风险评估矩阵 | ✅ |
| 估值钟形曲线 | 估值区间分析 | ✅ |
| 估值对比条形图 | 相对估值对比 | ✅ |

### 图表优化 (v2.1.0)

**主要改进**:
- ✨ 中文字体自动检测和配置
- ✨ 跨平台字体支持（macOS/Windows/Linux）
- ✨ 无GUI环境支持（服务器/Docker）
- 🐛 修复中文显示乱码问题
- 🐛 修复PDF生成中文问题
- ♻️ 添加数据验证和错误处理
- ♻️ 添加类型提示

详细的优化说明请参考 [CHART_OPTIMIZATION_SUMMARY.md](CHART_OPTIMIZATION_SUMMARY.md)

### Linux 字体安装

如果在Linux系统下图表中文显示为方块：

```bash
# Ubuntu/Debian
sudo apt-get install fonts-wqy-microhei fonts-noto-cjk

# CentOS/RHEL
sudo yum install wqy-microhei-fonts
```

## 📚 分析框架详解

完整的分析框架说明请参考 [docs/analysis_framework.md](docs/analysis_framework.md)

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## ⚠️ 免责声明

本工具生成的报告由AI根据公开文件生成，仅为基于"股票简化分析法"框架的研究分析，**不构成任何投资建议**。投资有风险，决策需谨慎。

## 🔗 相关资源

- [Gemini API 文档](https://ai.google.dev/docs)
- [Google AI Studio](https://aistudio.google.com/)
- [Tushare 数据平台](https://tushare.pro)

## 📮 联系方式

- **邮箱**: 1690295017@qq.com
- **微信**: yangbruant
- **GitHub Issues**: [提交问题](https://github.com/yanglaiyang/stock-analysis-skill/issues)

欢迎通过以上方式联系我，或直接提交 Issue 和 Pull Request！

---

**Made with ❤️ by yanglaiyang**
