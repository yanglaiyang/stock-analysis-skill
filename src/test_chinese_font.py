"""
测试中文字体在图表中的显示
"""

import sys
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent))

from font_config import configure_chinese_font, get_font_config
from chart_generator import StockChartGenerator
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def test_chinese_font_in_chart():
    """测试图表中的中文字体"""

    print("\n" + "="*60)
    print("中文字体图表测试")
    print("="*60)

    # 1. 配置字体
    print("\n步骤 1: 配置中文字体...")
    configure_chinese_font()

    font_config = get_font_config()
    font_name = font_config.available_chinese_font
    print(f"✓ 使用字体: {font_name}")

    # 2. 检查matplotlib配置
    print("\n步骤 2: 检查matplotlib配置...")
    print(f"  font.sans-serif: {plt.rcParams['font.sans-serif'][:3]}")
    print(f"  axes.unicode_minus: {plt.rcParams['axes.unicode_minus']}")

    # 3. 创建测试图表
    print("\n步骤 3: 创建测试图表...")
    output_dir = Path('test_output/font_test')
    output_dir.mkdir(parents=True, exist_ok=True)

    generator = StockChartGenerator(output_dir=str(output_dir), verbose=True)

    test_scores = {
        '业务阶段': 85,
        '护城河': 90,
        '财务健康': 85,
        '增长潜力': 65,
        '风险控制': 60
    }

    result = generator.create_investment_radar(test_scores)

    if result:
        print(f"\n✅ 图表生成成功: {result}")

        # 验证生成的图片
        from PIL import Image
        img = Image.open(result)
        print(f"  图片尺寸: {img.size}")
        print(f"  图片模式: {img.mode}")

        return True
    else:
        print("\n❌ 图表生成失败")
        return False


def test_all_text_elements():
    """测试所有文本元素的中文字体"""

    print("\n" + "="*60)
    print("测试所有文本元素")
    print("="*60)

    # 配置字体
    configure_chinese_font()
    font_config = get_font_config()
    font_name = font_config.available_chinese_font

    # 创建测试图
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor('#f8f9fa')

    # 测试数据
    x = [1, 2, 3, 4, 5]
    y = [10, 40, 60, 80, 95]

    # 绘制图表
    ax.plot(x, y, 'o-', linewidth=2, markersize=8, label='增长曲线')

    # 测试各种文本元素
    ax.set_title('股票增长趋势分析', fontsize=16, fontweight='bold',
                fontname=font_name, pad=20)
    ax.set_xlabel('时间周期', fontsize=12, fontname=font_name)
    ax.set_ylabel('股价 (元)', fontsize=12, fontname=font_name)

    ax.set_xticks(x)
    ax.set_xticklabels(['第1季度', '第2季度', '第3季度', '第4季度', '第5季度'],
                      fontsize=10, fontname=font_name)

    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels(['0', '20', '40', '60', '80', '100'],
                      fontsize=10, fontname=font_name)

    # 添加文本标注
    ax.text(3, 60, '关键增长点', fontsize=12, ha='center',
           fontname=font_name, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # 添加图例
    ax.legend(prop={'family': font_name, 'size': 10}, loc='upper left')

    # 添加网格
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('white')

    # 保存
    output_path = Path('test_output/font_test/所有文本元素测试.png')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✅ 测试图表已保存: {output_path}")
    print(f"\n请打开图片检查以下元素:")
    print(f"  - 标题: 股票增长趋势分析")
    print(f"  - X轴标签: 第1季度、第2季度等")
    print(f"  - Y轴标签: 股价 (元)")
    print(f"  - 刻度标签: 0, 20, 40等")
    print(f"  - 文本标注: 关键增长点")
    print(f"  - 图例: 增长曲线")

    return str(output_path)


if __name__ == '__main__':
    print("\n" + "="*70)
    print(" "*20 + "中文字体完整测试")
    print("="*70)

    # 测试1: 雷达图
    success1 = test_chinese_font_in_chart()

    # 测试2: 所有文本元素
    output2 = test_all_text_elements()

    # 总结
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)

    if success1:
        print("✅ 雷达图测试通过")
        print(f"✅ 所有文本元素测试通过: {output2}")
        print("\n请打开图片验证中文是否正常显示:")
        print("  open test_output/font_test/*.png")
    else:
        print("❌ 测试失败")

    print("="*70 + "\n")
