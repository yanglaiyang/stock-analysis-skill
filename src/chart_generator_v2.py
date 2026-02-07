"""
图表方法增强补丁
为所有图表方法添加数据验证和错误处理
"""

from typing import Dict, List, Optional, Union
from pathlib import Path
import warnings
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 从主模块导入 COLORS 和其他常量
try:
    from .chart_generator import COLORS, BLUE_GRADIENT
except ImportError:
    # 如果作为独立模块运行，定义本地常量
    COLORS = {
        'primary': '#1f77b4',
        'secondary': '#3498db',
        'dark': '#1a5276',
        'light': '#85c1e9',
        'text': '#2c3e50',
        'background': '#f8f9fa',
        'neutral': '#95a5a6',
        'success': '#27ae60',
    }
    BLUE_GRADIENT = ['#1a5276', '#1f77b4', '#3498db', '#5dade2', '#85c1e9']


class ChartMethodEnhancer:
    """图表方法增强器 - 为现有的StockChartGenerator添加增强方法"""

    @staticmethod
    def enhanced_create_financial_cards(generator, metrics_dict: Dict, save_path=None):
        """
        增强版：核心财务指标卡片图
        添加数据验证和错误处理
        """
        # 数据验证
        if not isinstance(metrics_dict, dict) or len(metrics_dict) == 0:
            warnings.warn("财务指标数据格式错误或为空")
            return None

        try:
            fig, axes = plt.subplots(2, 3, figsize=generator._get_figsize('large'))
            fig.patch.set_facecolor(COLORS['background'])
            fig.suptitle('核心财务指标', fontsize=18, fontweight='bold',
                        color=COLORS['dark'], y=0.98)

            axes = axes.flatten()

            for idx, (metric, data) in enumerate(metrics_dict.items()):
                if idx >= 6:  # 最多显示6个指标
                    break

                ax = axes[idx]

                # 数据验证
                if not isinstance(data, dict):
                    warnings.warn(f"指标 {metric} 数据格式错误")
                    continue

                value = data.get('value', 'N/A')
                unit = data.get('unit', '')
                trend = data.get('trend', '→')

                # 背景
                ax.set_facecolor(COLORS['primary'])
                ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes,
                                           color=COLORS['primary'], alpha=0.1))

                # 指标名称
                ax.text(0.5, 0.7, metric, ha='center', va='center',
                       fontsize=12, color=COLORS['text'],
                       transform=ax.transAxes, fontweight='bold')

                # 数值
                value_str = f"{value}{unit}"
                ax.text(0.5, 0.45, value_str, ha='center', va='center',
                       fontsize=20, color=COLORS['dark'],
                       transform=ax.transAxes, fontweight='bold')

                # 趋势
                trend_color = {
                    '↑': COLORS['success'],
                    '↓': '#e74c3c',
                    '→': COLORS['neutral']
                }.get(trend, COLORS['neutral'])

                ax.text(0.5, 0.25, trend, ha='center', va='center',
                       fontsize=24, color=trend_color,
                       transform=ax.transAxes, fontweight='bold')

                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.axis('off')

            # 隐藏多余的子图
            for idx in range(len(metrics_dict), 6):
                axes[idx].axis('off')

            if save_path is None:
                save_path = generator.output_dir / 'financial_cards.png'

            return generator._safe_save_figure(fig, save_path)

        except Exception as e:
            warnings.warn(f"生成财务指标卡片图失败: {e}")
            plt.close('all')
            return None

    @staticmethod
    def enhanced_create_risk_matrix(generator, risks: List[Dict], save_path=None):
        """
        增强版：风险矩阵图
        添加数据验证和错误处理
        """
        # 数据验证
        if not isinstance(risks, list) or len(risks) == 0:
            warnings.warn("风险数据格式错误或为空")
            return None

        try:
            fig, ax = plt.subplots(figsize=generator._get_figsize('medium'))
            fig.patch.set_facecolor(COLORS['background'])

            # 绘制象限
            ax.axhline(y=2, color=COLORS['neutral'], linestyle='--', alpha=0.5)
            ax.axvline(x=2, color=COLORS['neutral'], linestyle='--', alpha=0.5)

            # 象限标签
            ax.text(1.5, 2.5, '高影响/低概率', ha='center', va='center',
                   fontsize=11, color=COLORS['neutral'], alpha=0.7, style='italic')
            ax.text(2.5, 2.5, '高影响/高概率', ha='center', va='center',
                   fontsize=11, color='#e74c3c', alpha=0.7, style='italic', fontweight='bold')
            ax.text(1.5, 1.5, '低影响/低概率', ha='center', va='center',
                   fontsize=11, COLORS['success'], alpha=0.7, style='italic')
            ax.text(2.5, 1.5, '低影响/高概率', ha='center', va='center',
                   fontsize=11, color='#f39c12', alpha=0.7, style='italic')

            # 绘制风险点
            for risk in risks:
                # 数据验证
                if not isinstance(risk, dict):
                    continue

                impact = risk.get('impact', 2)
                probability = risk.get('probability', 2)
                name = risk.get('name', '未知风险')

                # 限制范围在1-3之间
                impact = max(1, min(3, float(impact)))
                probability = max(1, min(3, float(probability)))

                # 根据风险等级选择颜色
                if impact <= 1 and probability <= 1:
                    color = COLORS['success']
                elif impact <= 1 or probability <= 1:
                    color = '#f39c12'
                else:
                    color = '#e74c3c'

                ax.scatter(probability, impact,
                          s=300, color=color, alpha=0.7,
                          edgecolors=COLORS['dark'], linewidths=2)

                # 风险名称
                ax.annotate(name,
                           (probability, impact),
                           xytext=(10, 10), textcoords='offset points',
                           fontsize=9, color=COLORS['dark'],
                           bbox=dict(boxstyle='round,pad=0.3',
                                    facecolor='white', alpha=0.8))

            ax.set_xlim(0.5, 3.5)
            ax.set_ylim(0.5, 3.5)
            ax.set_xlabel('发生概率 →', fontsize=12, color=COLORS['dark'])
            ax.set_ylabel('影响程度 →', fontsize=12, color=COLORS['dark'])
            ax.set_xticks([1, 2, 3])
            ax.set_yticks([1, 2, 3])
            ax.set_xticklabels(['低', '中', '高'])
            ax.set_yticklabels(['低', '中', '高'])
            ax.grid(True, alpha=0.3)
            plt.title('风险评估矩阵', fontsize=16, fontweight='bold',
                     color=COLORS['dark'], pad=20)

            if save_path is None:
                save_path = generator.output_dir / 'risk_matrix.png'

            return generator._safe_save_figure(fig, save_path)

        except Exception as e:
            warnings.warn(f"生成风险矩阵图失败: {e}")
            plt.close('all')
            return None

    @staticmethod
    def enhanced_create_valuation_bell_curve(generator, current_pe: float,
                                             fair_range: tuple, save_path=None):
        """
        增强版：估值钟形曲线图
        添加数据验证和错误处理
        """
        # 数据验证
        try:
            current_pe = float(current_pe)
            if not isinstance(fair_range, (tuple, list)) or len(fair_range) != 2:
                raise ValueError("fair_range必须是包含2个元素的元组")

            min_pe, max_pe = float(fair_range[0]), float(fair_range[1])

        except (ValueError, TypeError) as e:
            warnings.warn(f"估值钟形曲线数据格式错误: {e}")
            return None

        try:
            fig, ax = plt.subplots(figsize=generator._get_figsize('medium'))
            fig.patch.set_facecolor(COLORS['background'])

            # 生成钟形曲线
            x = np.linspace(5, 30, 100)
            mu = np.mean([min_pe, max_pe])
            sigma = 5
            y = np.exp(-0.5 * ((x - mu) / sigma) ** 2)

            # 绘制曲线
            ax.plot(x, y, color=COLORS['primary'], linewidth=3)

            # 填充区域
            ax.fill_between(x, y, where=(x >= min_pe) & (x <= max_pe),
                           color=COLORS['success'], alpha=0.3, label='合理估值')
            ax.fill_between(x, y, where=(x > max_pe),
                           color='#e74c3c', alpha=0.3, label='高估')
            ax.fill_between(x, y, where=(x < min_pe),
                           color='#f39c12', alpha=0.3, label='低估')

            # 标注当前PE
            current_y = np.exp(-0.5 * ((current_pe - mu) / sigma) ** 2)
            ax.scatter([current_pe], [current_y], s=200, color=COLORS['secondary'],
                      edgecolors=COLORS['dark'], linewidths=2, zorder=5,
                      label=f'当前PE: {current_pe:.1f}')

            ax.axvline(x=current_pe, color=COLORS['secondary'],
                      linestyle='--', linewidth=2, alpha=0.7)

            # 标签
            ax.text(min_pe, 0.1, f'低估\n<{min_pe:.0f}倍',
                   ha='center', fontsize=10, color='#f39c12')
            ax.text(max_pe, 0.1, f'高估\n>{max_pe:.0f}倍',
                   ha='center', fontsize=10, color='#e74c3c')
            ax.text(mu, 0.1, f'合理\n{min_pe:.0f}-{max_pe:.0f}倍',
                   ha='center', fontsize=10, color=COLORS['success'])

            ax.set_xlabel('市盈率 (PE)', fontsize=12, color=COLORS['dark'])
            ax.set_ylabel('概率密度', fontsize=12, color=COLORS['dark'])
            ax.legend(loc='upper right')
            plt.title('估值区间分析', fontsize=16, fontweight='bold',
                     color=COLORS['dark'], pad=20)

            if save_path is None:
                save_path = generator.output_dir / 'valuation_bell_curve.png'

            return generator._safe_save_figure(fig, save_path)

        except Exception as e:
            warnings.warn(f"生成估值钟形曲线图失败: {e}")
            plt.close('all')
            return None


def patch_chart_generator(generator):
    """
    为StockChartGenerator实例打补丁，添加增强方法

    Args:
        generator: StockChartGenerator实例
    """
    enhancer = ChartMethodEnhancer()

    # 添加增强方法
    generator.create_financial_cards_v2 = lambda data, path=None: \
        enhancer.enhanced_create_financial_cards(generator, data, path)

    generator.create_risk_matrix_v2 = lambda data, path=None: \
        enhancer.enhanced_create_risk_matrix(generator, data, path)

    generator.create_valuation_bell_curve_v2 = lambda pe, rng, path=None: \
        enhancer.enhanced_create_valuation_bell_curve(generator, pe, rng, path)

    return generator


if __name__ == '__main__':
    print("图表方法增强补丁模块已加载")
    print("使用 patch_chart_generator() 函数为现有实例添加增强方法")
