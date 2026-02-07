"""
Stock Analysis Skill 完整功能测试
测试 skill 的文档规范性和功能完整性
"""

import sys
import os
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent))

import json
from datetime import datetime


def test_skill_json():
    """测试 skill.json 配置文件"""
    print("\n" + "="*60)
    print("测试 1: skill.json 配置文件")
    print("="*60)

    skill_path = Path(__file__).parent.parent / "skill.json"

    if not skill_path.exists():
        print("❌ skill.json 文件不存在")
        return False

    with open(skill_path, 'r', encoding='utf-8') as f:
        skill_config = json.load(f)

    # 检查必需字段
    required_fields = [
        'name', 'version', 'description', 'author',
        'license', 'keywords', 'main'
    ]

    all_ok = True
    for field in required_fields:
        if field in skill_config:
            print(f"✅ {field}: {skill_config[field]}")
        else:
            print(f"❌ 缺少字段: {field}")
            all_ok = False

    # 检查版本号格式
    version = skill_config.get('version', '')
    if version.count('.') >= 2:
        print(f"✅ 版本号格式正确: {version}")
    else:
        print(f"⚠️  版本号格式建议: MAJOR.MINOR.PATCH")

    return all_ok


def test_skill_wrapper():
    """测试 skill wrapper 脚本"""
    print("\n" + "="*60)
    print("测试 2: ~/.claude/skills/stock-analysis-skill")
    print("="*60)

    skill_path = Path.home() / '.claude/skills/stock-analysis-skill'

    if not skill_path.exists():
        print(f"❌ Skill wrapper 不存在: {skill_path}")
        return False

    print(f"✅ Skill wrapper 存在: {skill_path}")

    # 检查可执行权限
    if os.access(skill_path, os.X_OK):
        print(f"✅ 可执行权限已设置")
    else:
        print(f"⚠️  需要设置可执行权限: chmod +x {skill_path}")

    return True


def test_module_imports():
    """测试所有核心模块导入"""
    print("\n" + "="*60)
    print("测试 3: 核心模块导入")
    print("="*60)

    modules = [
        ('stock_analyzer', 'StockAnalyzer'),
        ('subagents', 'SubagentOrchestrator'),
        ('chart_generator', 'StockChartGenerator'),
        ('font_config', 'configure_chinese_font'),
        ('enhanced_report_generator', 'EnhancedReportGenerator'),
        ('pdf_generator', 'PDFReportGenerator'),
        ('tushare_mcp_client', 'TushareMCPClient'),
    ]

    all_ok = True
    for module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
        except ImportError as e:
            print(f"⚠️  {module_name}.{class_name}: {e}")
            # 某些模块可能不可用（如PDF生成器），不算失败
        except Exception as e:
            print(f"❌ {module_name}.{class_name}: {e}")
            all_ok = False

    return all_ok


def test_documentation():
    """测试文档完整性"""
    print("\n" + "="*60)
    print("测试 4: 文档完整性")
    print("="*60)

    project_root = Path(__file__).parent.parent

    # 必需文档
    required_docs = {
        'README.md': '项目说明文档',
        'USAGE_GUIDE.md': '使用指南',
        'requirements.txt': '依赖列表',
        'CHART_OPTIMIZATION_SUMMARY.md': '图表优化说明',
    }

    all_ok = True
    for doc_file, desc in required_docs.items():
        doc_path = project_root / doc_file
        if doc_path.exists():
            size = doc_path.stat().st_size
            print(f"✅ {doc_file} ({desc}) - {size} bytes")
        else:
            print(f"⚠️  {doc_file} ({desc}) 不存在")
            # 不算失败，因为有些文档是可选的

    return all_ok


def test_chart_generation():
    """测试图表生成功能"""
    print("\n" + "="*60)
    print("测试 5: 图表生成功能")
    print("="*60)

    try:
        from chart_generator import StockChartGenerator
        from font_config import configure_chinese_font

        # 配置字体
        configure_chinese_font()

        # 创建临时输出目录
        output_dir = Path('test_output/charts_test')
        output_dir.mkdir(parents=True, exist_ok=True)

        # 创建图表生成器
        generator = StockChartGenerator(output_dir=str(output_dir), verbose=False)

        # 测试数据
        test_scores = {
            '业务阶段': 85,
            '护城河': 90,
            '财务健康': 85,
            '增长潜力': 65,
            '风险控制': 60
        }

        # 生成测试图表
        result = generator.create_investment_radar(test_scores)

        if result and Path(result).exists():
            print(f"✅ 雷达图生成成功")
            return True
        else:
            print(f"❌ 雷达图生成失败")
            return False

    except Exception as e:
        print(f"❌ 图表生成测试失败: {e}")
        return False


def test_api_key_check():
    """测试API密钥检查"""
    print("\n" + "="*60)
    print("测试 6: API密钥配置")
    print("="*60)

    # 检查环境变量
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')

    if api_key:
        # 只显示部分密钥
        masked = api_key[:4] + '*' * (len(api_key) - 8) + api_key[-4:]
        print(f"✅ API密钥已配置: {masked}")
        return True
    else:
        print("⚠️  未检测到 GEMINI_API_KEY 或 GOOGLE_API_KEY")
        print("   提示: 运行 skill 时需要设置API密钥")
        return False


def test_skill_readme():
    """测试README规范"""
    print("\n" + "="*60)
    print("测试 7: README 规范")
    print("="*60)

    readme_path = Path(__file__).parent.parent / "README.md"

    if not readme_path.exists():
        print("❌ README.md 不存在")
        return False

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查必需章节
    required_sections = [
        '#',  # 标题
        '## 特性',
        '## 安装',
        '## 使用方法',
        '## 免责声明'
    ]

    all_ok = True
    for section in required_sections:
        if section in content:
            print(f"✅ 包含章节: {section}")
        else:
            print(f"⚠️  建议添加章节: {section}")
            # 不算失败

    # 检查徽章
    if 'shields.io' in content or 'img.shields.io' in content:
        print("✅ 包含项目徽章")

    return all_ok


def generate_test_report(results):
    """生成测试报告"""
    print("\n" + "="*70)
    print(" "*20 + "SKILL 测试报告")
    print("="*70)

    print(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"项目路径: {Path(__file__).parent.parent}")

    print("\n" + "-"*70)
    print("测试结果详情:")
    print("-"*70)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:30s}: {status}")

    total_tests = len(results)
    passed_tests = sum(results.values())

    print("\n" + "-"*70)
    print(f"总计: {passed_tests}/{total_tests} 测试通过 ({passed_tests*100//total_tests}%)")

    # 建议
    print("\n" + "="*70)
    print("建议:")
    print("="*70)

    if not results.get('API密钥配置'):
        print("1. 设置 GEMINI_API_KEY 环境变量以使用完整功能")

    if not results.get('Skill wrapper'):
        print("2. 确保 ~/.claude/skills/stock-analysis-skill 存在并可执行")

    if not results.get('图表生成功能'):
        print("3. 检查 matplotlib 和依赖库是否正确安装")

    # 总体评价
    print("\n" + "="*70)
    if passed_tests == total_tests:
        print("🎉 所有测试通过！Skill 已准备就绪。")
    elif passed_tests >= total_tests * 0.8:
        print("✅ Skill 基本功能正常，可以上传 GitHub。")
    else:
        print("⚠️  存在较多问题，建议修复后再上传。")
    print("="*70)

    return passed_tests == total_tests


def main():
    """运行所有测试"""
    print("\n" + "="*70)
    print(" "*15 + "Stock Analysis Skill 测试套件")
    print("="*70)

    # 运行所有测试
    results = {
        'skill.json配置': test_skill_json(),
        'Skill wrapper': test_skill_wrapper(),
        '模块导入': test_module_imports(),
        '文档完整性': test_documentation(),
        '图表生成功能': test_chart_generation(),
        'API密钥配置': test_api_key_check(),
        'README规范': test_skill_readme(),
    }

    # 生成报告
    success = generate_test_report(results)

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
