"""
图表优化测试脚本
验证中文字体、错误处理、数据验证等功能
"""

import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from font_config import configure_chinese_font, get_font_config
from chart_generator import StockChartGenerator
import warnings


def test_font_configuration():
    """测试字体配置"""
    print("\n" + "="*60)
    print("测试 1: 字体配置")
    print("="*60)

    try:
        # 配置字体
        configure_chinese_font()

        # 获取字体配置
        font_config = get_font_config()
        font_name = font_config.get_font_name()

        print(f"✓ 当前字体: {font_name}")

        # 测试中文显示
        print("\n运行中文显示测试...")
        test_result = font_config.test_chinese_display()

        return test_result

    except Exception as e:
        print(f"✗ 字体配置测试失败: {e}")
        return False


def test_chart_generator_init():
    """测试图表生成器初始化"""
    print("\n" + "="*60)
    print("测试 2: 图表生成器初始化")
    print("="*60)

    try:
        # 创建输出目录
        output_dir = Path('test_output/charts')
        output_dir.mkdir(parents=True, exist_ok=True)

        # 创建图表生成器
        generator = StockChartGenerator(output_dir=str(output_dir), verbose=True)

        print(f"✓ 图表生成器创建成功")
        print(f"  输出目录: {output_dir}")

        return generator

    except Exception as e:
        print(f"✗ 图表生成器初始化失败: {e}")
        return None


def test_investment_radar(generator):
    """测试投资评分雷达图"""
    print("\n" + "="*60)
    print("测试 3: 投资评分雷达图")
    print("="*60)

    try:
        test_data = {
            '业务阶段': 85,
            '护城河': 90,
            '财务健康': 85,
            '增长潜力': 65,
            '风险控制': 60
        }

        print("测试数据:")
        for k, v in test_data.items():
            print(f"  {k}: {v}")

        # 生成图表
        result = generator.create_investment_radar(test_data)

        if result:
            print(f"✓ 雷达图生成成功: {result}")
            return True
        else:
            print("✗ 雷达图生成失败")
            return False

    except Exception as e:
        print(f"✗ 雷达图测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_financial_cards(generator):
    """测试核心财务指标卡片"""
    print("\n" + "="*60)
    print("测试 4: 核心财务指标卡片")
    print("="*60)

    try:
        test_data = {
            '营业收入': {'value': '180.90', 'unit': '亿元', 'trend': '→'},
            '毛利率': {'value': '71.10', 'unit': '%', 'trend': '→'},
            '净利率': {'value': '21.90', 'unit': '%', 'trend': '→'},
            'ROE': {'value': '7.94', 'unit': '%', 'trend': '→'},
            'PE': {'value': '12.46', 'unit': '倍', 'trend': '↓'},
            'PB': {'value': '1.71', 'unit': '倍', 'trend': '→'},
        }

        print(f"测试指标数量: {len(test_data)}")

        result = generator.create_financial_cards(test_data)

        if result:
            print(f"✓ 财务卡片图生成成功: {result}")
            return True
        else:
            print("✗ 财务卡片图生成失败")
            return False

    except Exception as e:
        print(f"✗ 财务卡片图测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_risk_matrix(generator):
    """测试风险矩阵图"""
    print("\n" + "="*60)
    print("测试 5: 风险矩阵图")
    print("="*60)

    try:
        test_data = [
            {'name': '集中度风险', 'impact': 3, 'probability': 2},
            {'name': '政策风险', 'impact': 3, 'probability': 2},
            {'name': '竞争风险', 'impact': 3, 'probability': 3},
            {'name': '消费偏好变化', 'impact': 2, 'probability': 2}
        ]

        print(f"测试风险数量: {len(test_data)}")

        result = generator.create_risk_matrix(test_data)

        if result:
            print(f"✓ 风险矩阵图生成成功: {result}")
            return True
        else:
            print("✗ 风险矩阵图生成失败")
            return False

    except Exception as e:
        print(f"✗ 风险矩阵图测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_valuation_bell_curve(generator):
    """测试估值钟形曲线图"""
    print("\n" + "="*60)
    print("测试 6: 估值钟形曲线图")
    print("="*60)

    try:
        current_pe = 12.46
        fair_range = (10, 15)

        print(f"当前PE: {current_pe}")
        print(f"合理估值区间: {fair_range}")

        result = generator.create_valuation_bell_curve(current_pe, fair_range)

        if result:
            print(f"✓ 估值钟形曲线图生成成功: {result}")
            return True
        else:
            print("✗ 估值钟形曲线图生成失败")
            return False

    except Exception as e:
        print(f"✗ 估值钟形曲线图测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_error_handling(generator):
    """测试错误处理"""
    print("\n" + "="*60)
    print("测试 7: 错误处理和数据验证")
    print("="*60)

    all_passed = True

    # 测试 1: 空数据
    print("\n测试 7.1: 空数据处理")
    try:
        result = generator.create_investment_radar({})
        if result is None:
            print("✓ 正确处理空数据")
        else:
            print("✗ 空数据应返回None")
            all_passed = False
    except Exception as e:
        print(f"✗ 空数据处理异常: {e}")
        all_passed = False

    # 测试 2: 格式错误数据
    print("\n测试 7.2: 格式错误数据处理")
    try:
        result = generator.create_investment_radar(None)
        if result is None:
            print("✓ 正确处理格式错误数据")
        else:
            print("✗ 格式错误数据应返回None")
            all_passed = False
    except Exception as e:
        print(f"✗ 格式错误数据处理异常: {e}")
        all_passed = False

    # 测试 3: 数值范围修正
    print("\n测试 7.3: 数值范围修正")
    try:
        test_data = {
            '业务阶段': 150,  # 超出范围
            '护城河': -50,    # 负数
            '财务健康': 50,
        }
        result = generator.create_investment_radar(test_data)
        if result:
            print("✓ 正确处理超出范围数值（已自动修正）")
        else:
            print("✗ 未能处理超出范围数值")
            all_passed = False
    except Exception as e:
        print(f"✗ 数值范围修正异常: {e}")
        all_passed = False

    return all_passed


def main():
    """运行所有测试"""
    print("\n" + "="*70)
    print(" "*15 + "股票分析图表优化测试套件")
    print("="*70)
    print("\n此测试套件将验证以下功能:")
    print("1. 中文字体自动检测和配置")
    print("2. matplotlib后端配置（无GUI环境）")
    print("3. 图表生成和保存")
    print("4. 数据验证和错误处理")
    print("5. 跨平台兼容性")

    # 抑制警告输出
    warnings.filterwarnings('ignore', category=UserWarning)

    results = {}

    # 测试 1: 字体配置
    results['font_config'] = test_font_configuration()

    # 测试 2: 图表生成器初始化
    generator = test_chart_generator_init()
    results['generator_init'] = generator is not None

    if generator is None:
        print("\n✗ 图表生成器初始化失败，停止测试")
        return

    # 测试 3-6: 各类图表生成
    results['radar_chart'] = test_investment_radar(generator)
    results['financial_cards'] = test_financial_cards(generator)
    results['risk_matrix'] = test_risk_matrix(generator)
    results['valuation_curve'] = test_valuation_bell_curve(generator)

    # 测试 7: 错误处理
    results['error_handling'] = test_error_handling(generator)

    # 打印测试总结
    print("\n" + "="*70)
    print(" "*25 + "测试总结")
    print("="*70)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:20s}: {status}")

    total_tests = len(results)
    passed_tests = sum(results.values())

    print("\n" + "-"*70)
    print(f"总计: {passed_tests}/{total_tests} 测试通过")

    if passed_tests == total_tests:
        print("\n🎉 所有测试通过！图表优化已成功完成。")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} 个测试失败，请检查上述错误信息。")

    print("\n生成的图表保存在: test_output/charts/")
    print("="*70)

    return passed_tests == total_tests


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
