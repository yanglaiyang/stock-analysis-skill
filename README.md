# 📊 股票简化分析法 (Stock Simplified Analysis Method)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)

一个专业、系统化的股票分析工具，使用Gemini AI执行"股票简化分析法"七步分析框架，生成机构级股票分析报告。

## ✨ 特性

- 🎯 **七步系统化分析**: 从业务阶段到估值的完整分析框架
- 🤖 **AI驱动**: 基于Gemini AI的智能分析能力
- 📄 **多格式支持**: 支持PDF、HTML、URL等多种数据源
- 🔄 **自动重试**: 内置API限流处理机制
- 📝 **Markdown报告**: 生成格式精美的分析报告

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
git clone https://github.com/yourusername/stock-analysis-skill.git
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
│   └── stock_analyzer.py    # 主程序
├── tests/
│   └── test_analyzer.py     # 测试文件
├── docs/
│   └── analysis_framework.md # 分析框架文档
├── requirements.txt          # 依赖列表
├── README.md                # 本文件
└── skill.json              # Skill配置文件
```

### 运行测试

```bash
python tests/test_analyzer.py
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

如有问题或建议，请提交 [Issue](https://github.com/yourusername/stock-analysis-skill/issues)

---

**Made with ❤️ by Claude Code AI**
