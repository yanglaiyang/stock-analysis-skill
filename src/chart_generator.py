"""
Stock Analysis Chart Generator
生成专业的股票分析图表

特性：
- 蓝色商务风配色方案
- 15种专业图表类型
- 支持静态图片导出（PNG/SVG）
- 支持中文显示（自动字体检测）
- 跨平台支持（macOS/Windows/Linux）
- 无GUI环境支持
"""

import os
import sys
import matplotlib
matplotlib.use('Agg')  # 设置为无GUI后端

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from pathlib import Path
import warnings
from typing import Dict, List, Optional, Any, Union

# 导入字体配置模块
try:
    from font_config import configure_chinese_font, get_font_config
    # 配置中文字体
    configure_chinese_font()

    # 获取配置的字体名称
    font_config = get_font_config()
    CHINESE_FONT = font_config.available_chinese_font if font_config else 'Arial Unicode MS'

    # 强制设置matplotlib字体
    plt.rcParams['font.sans-serif'] = [CHINESE_FONT, 'SimHei', 'DejaVu Sans', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.family'] = 'sans-serif'

    # 提高图表质量和抗锯齿
    plt.rcParams['figure.dpi'] = 150
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['path.simplify'] = False
    plt.rcParams['path.sketch'] = None

    # 抗锯齿设置（兼容不同matplotlib版本）
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3

    # 字体大小和线条设置
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['grid.linewidth'] = 0.5

    FONT_AVAILABLE = True
    print(f"✓ 图表生成器使用字体: {CHINESE_FONT}")
    print(f"✓ 图表质量设置: 300 DPI")
except ImportError:
    print("⚠️ 字体配置模块不可用，使用默认配置")
    FONT_AVAILABLE = False
    CHINESE_FONT = 'Arial Unicode MS'
    # 回退到原配置
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

# 蓝色商务风配色方案
COLORS = {
    'primary': '#1f77b4',      # 主蓝色
    'secondary': '#3498db',    # 次蓝色
    'accent': '#0066cc',       # 强调蓝
    'dark': '#1a5276',         # 深蓝
    'light': '#85c1e9',        # 浅蓝
    'success': '#27ae60',      # 成功绿
    'warning': '#f39c12',      # 警告橙
    'danger': '#e74c3c',       # 危险红
    'neutral': '#95a5a6',      # 中性灰
    'background': '#f8f9fa',   # 背景白
    'text': '#2c3e50',         # 文字黑
}

# 渐变蓝色
BLUE_GRADIENT = [
    '#1a5276',  # 深蓝
    '#1f77b4',  # 主蓝
    '#3498db',  # 次蓝
    '#5dade2',  # 中蓝
    '#85c1e9',  # 浅蓝
    '#aed6f1',  # 极浅蓝
]

# 评分颜色
SCORE_COLORS = {
    'excellent': '#27ae60',  # 优秀 - 绿
    'good': '#3498db',       # 良好 - 蓝
    'average': '#f39c12',    # 一般 - 橙
    'poor': '#e74c3c',       # 较差 - 红
}


class StockChartGenerator:
    """股票分析图表生成器"""

    def __init__(self, output_dir='charts', verbose=True):
        """
        初始化图表生成器

        Args:
            output_dir: 图表输出目录
            verbose: 是否打印详细信息
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose

        # 设置seaborn样式
        sns.set_style("whitegrid")
        sns.set_palette("husl")

        # 强制应用中文字体（防止被样式覆盖）
        try:
            mpl.rcParams['font.sans-serif'] = [CHINESE_FONT, 'Arial Unicode MS', 'SimHei', 'DejaVu Sans', 'Arial']
            mpl.rcParams['font.family'] = 'sans-serif'
            mpl.rcParams['axes.unicode_minus'] = False
            sns.set_theme(style="whitegrid", font=CHINESE_FONT)
        except Exception:
            pass

        # 测试中文支持
        if self.verbose:
            self._test_chinese_support()

    def _test_chinese_support(self):
        """测试中文支持"""
        try:
            fig, ax = plt.subplots(figsize=(1, 1))
            ax.text(0.5, 0.5, '测试', ha='center')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            plt.close(fig)

            if FONT_AVAILABLE:
                font_name = get_font_config().get_font_name()
                print(f"✓ 中文字体支持已启用: {font_name}")
            else:
                print("⚠ 中文字体配置可能存在问题")
        except Exception as e:
            warnings.warn(f"中文测试失败: {e}")

    def _validate_data(self, data: Dict, required_keys: List[str] = None) -> bool:
        """
        验证数据格式

        Args:
            data: 待验证的数据
            required_keys: 必需的键列表

        Returns:
            验证是否通过
        """
        if not isinstance(data, dict):
            if self.verbose:
                warnings.warn(f"数据格式错误: 期望dict, 实际{type(data)}")
            return False

        if required_keys:
            missing_keys = [k for k in required_keys if k not in data]
            if missing_keys:
                if self.verbose:
                    warnings.warn(f"缺少必需的键: {missing_keys}")
                return False

        return True

    def _safe_save_figure(self, fig, save_path: Union[str, Path],
                         dpi: int = 300, tight: bool = True) -> Optional[str]:
        """
        安全保存图表

        Args:
            fig: matplotlib图表对象
            save_path: 保存路径
            dpi: 分辨率
            tight: 是否使用tight布局

        Returns:
            保存的文件路径，失败则返回None
        """
        try:
            save_path = Path(save_path)
            plt.tight_layout() if tight else None

            fig.savefig(
                save_path,
                dpi=dpi,
                bbox_inches='tight' if tight else None,
                facecolor=fig.get_facecolor(),
                edgecolor='none',
                pil_kwargs={'optimize': True, 'quality': 95}
            )
            plt.close(fig)

            if self.verbose:
                print(f"  ✓ 图表已保存: {save_path.name}")

            return str(save_path)

        except Exception as e:
            warnings.warn(f"保存图表失败: {e}")
            plt.close(fig)
            return None

    def _get_figsize(self, size='medium'):
        """获取图表尺寸"""
        sizes = {
            'small': (8, 6),
            'medium': (12, 8),
            'large': (16, 10),
            'wide': (16, 6),
        }
        return sizes.get(size, (12, 8))

    # ========================================
    # 1. 投资仪表盘雷达图
    # ========================================
    def create_investment_radar(self, scores_dict: Dict[str, float],
                                save_path: Optional[Union[str, Path]] = None) -> Optional[str]:
        """
        创建投资评分雷达图

        Args:
            scores_dict: {'维度名': 分数(0-100)}
            save_path: 保存路径

        Returns:
            保存的文件路径，失败则返回None
        """
        # 数据验证
        if not self._validate_data(scores_dict):
            return None

        if len(scores_dict) < 3:
            warnings.warn("雷达图至少需要3个维度")
            return None

        try:
            categories = list(scores_dict.keys())
            values = list(scores_dict.values())

            # 验证数值范围
            values = [max(0, min(100, float(v))) for v in values]  # 限制在0-100之间

            # 闭合雷达图
            values_closed = values + [values[0]]
            categories_closed = categories + [categories[0]]

            fig, ax = plt.subplots(figsize=self._get_figsize('medium'))
            fig.patch.set_facecolor(COLORS['background'])

            # 计算角度
            angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
            angles_closed = angles + [angles[0]]

            # 绘制雷达图
            ax = plt.subplot(111, polar=True)
            ax.plot(angles_closed, values_closed, 'o-', linewidth=2,
                    color=COLORS['primary'], label='当前评分')
            ax.fill(angles_closed, values_closed, alpha=0.25, color=COLORS['primary'])

            # 添加参考线（优秀线）
            ax.fill(angles, [80]*len(categories), alpha=0.1, color=COLORS['success'])

            # 设置刻度和标签 - 明确指定字体
            ax.set_xticks(angles)
            ax.set_xticklabels(categories, fontsize=11, color=COLORS['text'],
                             fontname=CHINESE_FONT)
            ax.set_ylim(0, 100)
            ax.set_yticks([20, 40, 60, 80, 100])
            ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=9,
                             fontname=CHINESE_FONT)
            ax.grid(True, color=COLORS['neutral'], alpha=0.3)

            # 添加标题 - 明确指定字体
            plt.title('投资评分仪表盘', fontsize=16, fontweight='bold',
                     color=COLORS['dark'], pad=20, fontname=CHINESE_FONT)

            # 添加图例 - 明确指定字体
            legend = plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1),
                              prop={'family': CHINESE_FONT, 'size': 10})

            # 保存
            if save_path is None:
                save_path = self.output_dir / 'investment_radar.png'

            return self._safe_save_figure(fig, save_path)

        except Exception as e:
            warnings.warn(f"生成投资评分雷达图失败: {e}")
            return None

    # ========================================
    # 2. 核心财务指标卡片图
    # ========================================
    def create_financial_cards(self, metrics_dict, save_path=None):
        """
        创建核心财务指标卡片图

        Args:
            metrics_dict: {'指标名': {'value': 数值, 'unit': 单位, 'trend': '↑↓→'}}
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        fig, axes = plt.subplots(2, 3, figsize=self._get_figsize('large'))
        fig.patch.set_facecolor(COLORS['background'])
        fig.suptitle('核心财务指标', fontsize=18, fontweight='bold',
                    color=COLORS['dark'], y=0.98)

        axes = axes.flatten()

        for idx, (metric, data) in enumerate(metrics_dict.items()):
            ax = axes[idx]

            # 背景
            ax.set_facecolor(COLORS['primary'])
            ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes,
                                       color=COLORS['primary'], alpha=0.1))

            # 指标名称
            ax.text(0.5, 0.7, metric, ha='center', va='center',
                   fontsize=12, color=COLORS['text'],
                   transform=ax.transAxes, fontweight='bold')

            # 数值
            value_str = f"{data['value']}{data.get('unit', '')}"
            ax.text(0.5, 0.45, value_str, ha='center', va='center',
                   fontsize=20, color=COLORS['dark'],
                   transform=ax.transAxes, fontweight='bold')

            # 趋势
            trend = data.get('trend', '→')
            trend_color = {
                '↑': COLORS['success'],
                '↓': COLORS['danger'],
                '→': COLORS['neutral']
            }.get(trend, COLORS['neutral'])

            ax.text(0.5, 0.25, trend, ha='center', va='center',
                   fontsize=24, color=trend_color,
                   transform=ax.transAxes, fontweight='bold')

            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')

        # 隐藏多余的子图
        for idx in range(len(metrics_dict), len(axes)):
            axes[idx].axis('off')

        # 保存
        if save_path is None:
            save_path = self.output_dir / 'financial_cards.png'
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'])
        plt.close()

        return str(save_path)

    # ========================================
    # 3. 业务阶段时间轴图
    # ========================================
    def create_business_stage_timeline(self, current_stage, stages_data, save_path=None):
        """
        创建业务阶段时间轴图

        Args:
            current_stage: 当前阶段名称
            stages_data: [{'name': '阶段名', 'desc': '描述'}, ...]
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        fig, ax = plt.subplots(figsize=self._get_figsize('wide'))
        fig.patch.set_facecolor(COLORS['background'])

        n_stages = len(stages_data)
        x_positions = np.arange(n_stages)

        # 绘制时间轴线
        ax.plot([0, n_stages-1], [1, 1], color=COLORS['neutral'],
               linewidth=3, alpha=0.5, zorder=1)

        # 绘制各阶段
        for idx, stage in enumerate(stages_data):
            x = x_positions[idx]
            is_current = (stage['name'] == current_stage)

            # 阶段点
            color = COLORS['primary'] if is_current else COLORS['light']
            size = 400 if is_current else 250
            ax.scatter(x, 1, s=size, color=color, zorder=2,
                      edgecolors=COLORS['dark'], linewidths=2)

            # 阶段名称
            fontweight = 'bold' if is_current else 'normal'
            fontsize = 13 if is_current else 11
            ax.text(x, 1.3, stage['name'], ha='center', va='bottom',
                   fontsize=fontsize, fontweight=fontweight,
                   color=COLORS['dark'])

            # 阶段描述
            if is_current:
                ax.text(x, 0.7, '✓ 当前', ha='center', va='top',
                       fontsize=12, fontweight='bold',
                       color=COLORS['success'])

            # 详细描述
            ax.text(x, 0.5, stage.get('desc', ''), ha='center', va='top',
                   fontsize=9, color=COLORS['text'],
                   wrap=True)

        ax.set_xlim(-0.5, n_stages - 0.5)
        ax.set_ylim(0, 1.5)
        ax.axis('off')
        plt.title('业务发展阶段', fontsize=16, fontweight='bold',
                 color=COLORS['dark'], pad=20)

        # 保存
        if save_path is None:
            save_path = self.output_dir / 'business_stage_timeline.png'
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'])
        plt.close()

        return str(save_path)

    # ========================================
    # 4. 商业画布图
    # ========================================
    def create_business_canvas(self, canvas_data, save_path=None):
        """
        创建商业画布图

        Args:
            canvas_data: 商业画布数据字典
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        fig, ax = plt.subplots(figsize=self._get_figsize('large'))
        fig.patch.set_facecolor(COLORS['background'])

        # 定义9个模块的位置
        positions = {
            'key_partners': (0, 2),
            'key_activities': (1, 2),
            'key_resources': (2, 2),
            'value_propositions': (1, 1),
            'customer_relationships': (0, 0),
            'channels': (1, 0),
            'customer_segments': (2, 0),
            'cost_structure': (0, -1),
            'revenue_streams': (2, -1),
        }

        labels = {
            'key_partners': '关键合作伙伴',
            'key_activities': '关键业务',
            'key_resources': '核心资源',
            'value_propositions': '价值主张',
            'customer_relationships': '客户关系',
            'channels': '渠道通路',
            'customer_segments': '客户细分',
            'cost_structure': '成本结构',
            'revenue_streams': '收入来源',
        }

        # 绘制9个模块
        for key, (x, y) in positions.items():
            # 框
            rect = plt.Rectangle((x-0.45, y-0.4), 0.9, 0.8,
                                facecolor=BLUE_GRADIENT[2],
                                edgecolor=COLORS['dark'],
                                linewidth=2, alpha=0.3)
            ax.add_patch(rect)

            # 标题
            ax.text(x, y+0.25, labels[key], ha='center', va='center',
                   fontsize=10, fontweight='bold', color=COLORS['dark'])

            # 内容
            content = canvas_data.get(key, [])
            if isinstance(content, list):
                content_text = '\n'.join([f'• {item}' for item in content[:3]])
            else:
                content_text = str(content)

            ax.text(x, y-0.1, content_text, ha='center', va='center',
                   fontsize=8, color=COLORS['text'])

        ax.set_xlim(-1, 3)
        ax.set_ylim(-1.5, 2.5)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.title('商业模式画布', fontsize=16, fontweight='bold',
                 color=COLORS['dark'], pad=20)

        # 保存
        if save_path is None:
            save_path = self.output_dir / 'business_canvas.png'
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'])
        plt.close()

        return str(save_path)

    # ========================================
    # 5. 产品矩阵象限图
    # ========================================
    def create_product_portfolio(self, products, save_path=None):
        """
        创建产品矩阵象限图

        Args:
            products: [{'name': '产品名', 'x': 市场份额, 'y': 价格, 'size': 销售额}]
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        fig, ax = plt.subplots(figsize=self._get_figsize('medium'))
        fig.patch.set_facecolor(COLORS['background'])

        # 绘制象限
        ax.axhline(y=0.5, color=COLORS['neutral'], linestyle='--', alpha=0.5)
        ax.axvline(x=0.5, color=COLORS['neutral'], linestyle='--', alpha=0.5)

        # 绘制产品
        for product in products:
            ax.scatter(product['x'], product['y'],
                      s=product.get('size', 100) * 3,
                      color=BLUE_GRADIENT[2],
                      alpha=0.6, edgecolors=COLORS['dark'], linewidths=2)

            # 产品名称
            ax.annotate(product['name'],
                       (product['x'], product['y']),
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=10, color=COLORS['dark'])

        # 象限标签
        ax.text(0.25, 0.75, '低端/高份额', ha='center', va='center',
               fontsize=12, color=COLORS['neutral'], alpha=0.5)
        ax.text(0.75, 0.75, '高端/高份额', ha='center', va='center',
               fontsize=12, color=COLORS['neutral'], alpha=0.5)
        ax.text(0.25, 0.25, '低端/低份额', ha='center', va='center',
               fontsize=12, color=COLORS['neutral'], alpha=0.5)
        ax.text(0.75, 0.25, '高端/低份额', ha='center', va='center',
               fontsize=12, color=COLORS['neutral'], alpha=0.5)

        # 轴标签
        ax.set_xlabel('品牌力 / 市场份额', fontsize=12, color=COLORS['dark'])
        ax.set_ylabel('价格定位', fontsize=12, color=COLORS['dark'])

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        plt.title('产品矩阵分析', fontsize=16, fontweight='bold',
                 color=COLORS['dark'], pad=20)

        # 保存
        if save_path is None:
            save_path = self.output_dir / 'product_portfolio.png'
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'])
        plt.close()

        return str(save_path)

    # ========================================
    # 6. 护城河雷达图
    # ========================================
    def create_moat_radar(self, moat_scores, save_path=None):
        """
        创建护城河雷达图

        Args:
            moat_scores: {'品牌价值': 95, '规模效应': 85, ...}
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        return self.create_investment_radar(moat_scores, save_path)

    # ========================================
    # 7. 护城河瀑布图
    # ========================================
    def create_moat_waterfall(self, moat_components, save_path=None):
        """
        创建护城河构成瀑布图

        Args:
            moat_components: [{'name': '名称', 'value': 百分比}, ...]
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        fig, ax = plt.subplots(figsize=self._get_figsize('wide'))
        fig.patch.set_facecolor(COLORS['background'])

        # 计算累积值
        x = np.arange(len(moat_components))
        values = [c['value'] for c in moat_components]
        cumulative = np.cumsum([0] + values[:-1])

        # 绘制瀑布图
        bars = ax.bar(x, values, bottom=cumulative,
                     color=BLUE_GRADIENT[:len(moat_components)],
                     edgecolor=COLORS['dark'], linewidth=1.5, alpha=0.8)

        # 数值标签
        for i, (bar, value) in enumerate(zip(bars, values)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, cumulative[i] + height/2,
                   f'{value}%', ha='center', va='center',
                   fontsize=11, fontweight='bold', color='white')

        # X轴标签
        ax.set_xticks(x)
        ax.set_xticklabels([c['name'] for c in moat_components],
                          fontsize=11, color=COLORS['text'])
        ax.set_xlabel('护城河构成', fontsize=12, color=COLORS['dark'])
        ax.set_ylabel('贡献度 (%)', fontsize=12, color=COLORS['dark'])

        ax.grid(axis='y', alpha=0.3)
        plt.title('护城河构成分析', fontsize=16, fontweight='bold',
                 color=COLORS['dark'], pad=20)

        # 保存
        if save_path is None:
            save_path = self.output_dir / 'moat_waterfall.png'
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'])
        plt.close()

        return str(save_path)

    # ========================================
    # 8. 财务指标热力图
    # ========================================
    def create_financial_heatmap(self, heatmap_data, save_path=None):
        """
        创建财务指标热力图

        Args:
            heatmap_data: DataFrame或二维数组，行=指标，列=评分维度
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        fig, ax = plt.subplots(figsize=self._get_figsize('medium'))
        fig.patch.set_facecolor(COLORS['background'])

        # 转换为DataFrame
        if not isinstance(heatmap_data, pd.DataFrame):
            heatmap_data = pd.DataFrame(heatmap_data)

        # 绘制热力图
        sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='RdYlGn',
                   center=50, vmin=0, vmax=100,
                   cbar_kws={'label': '评分'},
                   linewidths=1, linecolor='white',
                   ax=ax, annot_kws={'family': 'sans-serif', 'size': 11})

        ax.set_xlabel('评估维度', fontsize=12, color=COLORS['dark'], fontfamily='sans-serif')
        ax.set_ylabel('财务指标', fontsize=12, color=COLORS['dark'], fontfamily='sans-serif')
        plt.title('财务健康度热力图', fontsize=16, fontweight='bold',
                 color=COLORS['dark'], pad=20, fontfamily='sans-serif')

        # 保存
        if save_path is None:
            save_path = self.output_dir / 'financial_heatmap.png'
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'], edgecolor='none',
                   pil_kwargs={'optimize': True})
        plt.close()

        return str(save_path)

    # ========================================
    # 9. 杜邦分析树状图
    # ========================================
    def create_dupont_analysis(self, dupont_data, save_path=None):
        """
        创建杜邦分析树状图

        Args:
            dupont_data: 杜邦分析数据字典
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        fig, ax = plt.subplots(figsize=self._get_figsize('large'))
        fig.patch.set_facecolor(COLORS['background'])

        # 层级结构
        levels = [
            [dupont_data['roe']],  # ROE
            [
                dupont_data['net_margin'],
                dupont_data['asset_turnover'],
                dupont_data['equity_multiplier']
            ],
            # 第三层（根据净利率拆分）
            [
                dupont_data.get('gross_margin', 0),
                dupont_data.get('expense_ratio', 0),
                0, 0  # 占位
            ],
        ]

        # 绘制树状图
        y_offsets = [2, 1, 0]

        for level_idx, level in enumerate(levels):
            y = y_offsets[level_idx]
            n_items = len(level)
            x_positions = np.linspace(0, 1, n_items + 2)[1:-1]

            for x, value in zip(x_positions, level):
                if value == 0:
                    continue

                # 绘制节点
                circle = plt.Circle((x, y), 0.08,
                                  facecolor=BLUE_GRADIENT[level_idx],
                                  edgecolor=COLORS['dark'], linewidth=2)
                ax.add_patch(circle)

                # 数值标签
                ax.text(x, y, f'{value:.1%}%', ha='center', va='center',
                       fontsize=10, fontweight='bold', color='white')

                # 连接线
                if level_idx > 0:
                    parent_x = 0.5  # 上一层的中心
                    parent_y = y_offsets[level_idx - 1]
                    ax.plot([parent_x, x], [parent_y, y],
                           color=COLORS['neutral'], linewidth=1.5, alpha=0.5)

        # 添加标签
        ax.text(0.5, 2.15, 'ROE', ha='center', fontsize=12,
               fontweight='bold', color=COLORS['dark'])
        ax.text(0.5, 1.15, '净利率×总资产周转率×权益乘数',
               ha='center', fontsize=10, color=COLORS['text'])

        ax.set_xlim(-0.2, 1.2)
        ax.set_ylim(-0.3, 2.3)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.title('杜邦分析 - ROE拆解', fontsize=16, fontweight='bold',
                 color=COLORS['dark'], pad=20)

        # 保存
        if save_path is None:
            save_path = self.output_dir / 'dupont_analysis.png'
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'])
        plt.close()

        return str(save_path)

    # ========================================
    # 10. 现金流桑基图
    # ========================================
    def create_cashflow_sankey(self, flow_data, save_path=None):
        """
        创建现金流桑基图（简化版，使用堆叠条形图）

        Args:
            flow_data: 现金流数据
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        fig, ax = plt.subplots(figsize=self._get_figsize('wide'))
        fig.patch.set_facecolor(COLORS['background'])

        stages = flow_data.get('stages', [])
        flows = flow_data.get('flows', [])

        # 绘制简化的桑基图（堆叠条形图）
        y_positions = np.arange(len(stages))

        for i, stage in enumerate(stages):
            if i == 0:
                # 第一阶段
                values = [stage['value']]
                colors = [BLUE_GRADIENT[0]]
                bottom = 0
            else:
                # 后续阶段
                values = stage['components']
                colors = BLUE_GRADIENT[:len(values)]
                bottom = 0

            # 绘制堆叠条形
            left = 0
            for value, color in zip(values, colors):
                ax.barh(i, value, left=left, height=0.5,
                       color=color, edgecolor=COLORS['dark'], linewidth=1,
                       label=f'{value:.1%}' if i == 0 else '')
                left += value

            # 标签
            ax.text(left + 0.02, i, stage['name'],
                   va='center', fontsize=11, fontweight='bold',
                   color=COLORS['dark'])

        ax.set_yticks(y_positions)
        ax.set_yticklabels([s['name'] for s in stages])
        ax.set_xlabel('金额（亿元）', fontsize=12, color=COLORS['dark'])
        plt.title('现金流分析', fontsize=16, fontweight='bold',
                 color=COLORS['dark'], pad=20)

        # 保存
        if save_path is None:
            save_path = self.output_dir / 'cashflow_sankey.png'
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'])
        plt.close()

        return str(save_path)

    # ========================================
    # 11. 增长驱动力树状图
    # ========================================
    def create_growth_tree(self, growth_data, save_path=None):
        """
        创建增长驱动力树状图

        Args:
            growth_data: 增长驱动力数据
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        fig, ax = plt.subplots(figsize=self._get_figsize('large'))
        fig.patch.set_facecolor(COLORS['background'])

        # 根节点
        ax.text(0.5, 3, '未来增长\n100%', ha='center', va='center',
               fontsize=14, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor=BLUE_GRADIENT[0],
                        edgecolor=COLORS['dark'], linewidth=2),
               color='white')

        # 第一层驱动力
        level1 = growth_data.get('level1', [])
        y_pos = 2
        x_positions = np.linspace(0.1, 0.9, len(level1))

        for idx, driver in enumerate(level1):
            x = x_positions[idx]

            # 连接线
            ax.plot([0.5, x], [2.8, y_pos + 0.3],
                   color=COLORS['neutral'], linewidth=2, alpha=0.5)

            # 节点
            ax.text(x, y_pos,
                   f"{driver['name']}\n{driver.get('percentage', '')}",
                   ha='center', va='center', fontsize=11,
                   bbox=dict(boxstyle='round', facecolor=BLUE_GRADIENT[1],
                            edgecolor=COLORS['dark'], linewidth=1.5),
                   color='white')

            # 第二层驱动因子
            if 'factors' in driver:
                y_pos2 = 1
                x_positions2 = np.linspace(x - 0.15, x + 0.15, len(driver['factors']))

                for idx2, factor in enumerate(driver['factors']):
                    x2 = x_positions2[idx2]

                    # 连接线
                    ax.plot([x, x2], [y_pos - 0.3, y_pos2 + 0.25],
                           color=COLORS['neutral'], linewidth=1, alpha=0.5)

                    # 节点
                    ax.text(x2, y_pos2, factor['name'],
                           ha='center', va='center', fontsize=9,
                           bbox=dict(boxstyle='round', facecolor=BLUE_GRADIENT[2],
                                   edgecolor=COLORS['dark'], linewidth=1),
                           color=COLORS['dark'])

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 3.2)
        ax.axis('off')
        plt.title('增长驱动力分析', fontsize=16, fontweight='bold',
                 color=COLORS['dark'], pad=20)

        # 保存
        if save_path is None:
            save_path = self.output_dir / 'growth_tree.png'
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'])
        plt.close()

        return str(save_path)

    # ========================================
    # 12. 增长阶段曲线图
    # ========================================
    def create_growth_curve(self, growth_stages, current_stage, save_path=None):
        """
        创建增长阶段曲线图

        Args:
            growth_stages: 增长阶段数据
            current_stage: 当前阶段
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        fig, ax = plt.subplots(figsize=self._get_figsize('wide'))
        fig.patch.set_facecolor(COLORS['background'])

        # 生成S型曲线
        x = np.linspace(0, 10, 100)
        y = 100 / (1 + np.exp(-1.5 * (x - 5)))

        # 绘制曲线
        ax.plot(x, y, color=COLORS['primary'], linewidth=3,
               label='增长轨迹')

        # 标注阶段
        stage_positions = {
            'startup': (1, 15),
            'growth': (4, 50),
            'mature': (7, 85),
            'decline': (9, 95)
        }

        for stage, (x_pos, y_pos) in stage_positions.items():
            is_current = (stage == current_stage)
            color = COLORS['success'] if is_current else COLORS['light']
            size = 150 if is_current else 100

            ax.scatter(x_pos, y_pos, s=size, color=color,
                      edgecolors=COLORS['dark'], linewidths=2,
                      zorder=5, label=stage)

            # 标签
            fontweight = 'bold' if is_current else 'normal'
            ax.text(x_pos, y_pos - 10, stage.title(),
                   ha='center', fontsize=10, fontweight=fontweight,
                   color=COLORS['dark'])

        ax.set_xlabel('时间', fontsize=12, color=COLORS['dark'])
        ax.set_ylabel('价值', fontsize=12, color=COLORS['dark'])
        ax.grid(True, alpha=0.3)
        plt.title('增长阶段曲线', fontsize=16, fontweight='bold',
                 color=COLORS['dark'], pad=20)

        # 保存
        if save_path is None:
            save_path = self.output_dir / 'growth_curve.png'
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'])
        plt.close()

        return str(save_path)

    # ========================================
    # 13. 风险矩阵图
    # ========================================
    def create_risk_matrix(self, risks, save_path=None):
        """
        创建风险矩阵图

        Args:
            risks: [{'name': '风险名', 'impact': 影响(1-3), 'probability': 概率(1-3)}]
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        fig, ax = plt.subplots(figsize=self._get_figsize('medium'))
        fig.patch.set_facecolor(COLORS['background'])

        # 绘制象限
        ax.axhline(y=2, color=COLORS['neutral'], linestyle='--', alpha=0.5)
        ax.axvline(x=2, color=COLORS['neutral'], linestyle='--', alpha=0.5)

        # 象限标签
        ax.text(1.5, 2.5, '高影响/低概率', ha='center', va='center',
               fontsize=11, color=COLORS['neutral'], alpha=0.7, style='italic')
        ax.text(2.5, 2.5, '高影响/高概率', ha='center', va='center',
               fontsize=11, color=COLORS['danger'], alpha=0.7, style='italic', fontweight='bold')
        ax.text(1.5, 1.5, '低影响/低概率', ha='center', va='center',
               fontsize=11, color=COLORS['success'], alpha=0.7, style='italic')
        ax.text(2.5, 1.5, '低影响/高概率', ha='center', va='center',
               fontsize=11, color=COLORS['warning'], alpha=0.7, style='italic')

        # 绘制风险点
        for risk in risks:
            color = COLORS['danger']
            if risk['impact'] <= 1 and risk['probability'] <= 1:
                color = COLORS['success']
            elif risk['impact'] <= 1 or risk['probability'] <= 1:
                color = COLORS['warning']

            ax.scatter(risk['probability'], risk['impact'],
                      s=300, color=color, alpha=0.7,
                      edgecolors=COLORS['dark'], linewidths=2)

            # 风险名称
            ax.annotate(risk['name'],
                       (risk['probability'], risk['impact']),
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

        # 保存
        if save_path is None:
            save_path = self.output_dir / 'risk_matrix.png'
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'])
        plt.close()

        return str(save_path)

    # ========================================
    # 14. 估值钟形曲线图
    # ========================================
    def create_valuation_bell_curve(self, current_pe, fair_range, save_path=None):
        """
        创建估值钟形曲线图

        Args:
            current_pe: 当前PE
            fair_range: (min_pe, max_pe) 合理估值区间
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        fig, ax = plt.subplots(figsize=self._get_figsize('medium'))
        fig.patch.set_facecolor(COLORS['background'])

        # 生成钟形曲线
        x = np.linspace(5, 30, 100)
        mu = np.mean(fair_range)
        sigma = 5
        y = np.exp(-0.5 * ((x - mu) / sigma) ** 2)

        # 绘制曲线
        ax.plot(x, y, color=COLORS['primary'], linewidth=3)

        # 填充区域
        ax.fill_between(x, y, where=(x >= fair_range[0]) & (x <= fair_range[1]),
                       color=COLORS['success'], alpha=0.3, label='合理估值')
        ax.fill_between(x, y, where=(x > fair_range[1]),
                       color=COLORS['danger'], alpha=0.3, label='高估')
        ax.fill_between(x, y, where=(x < fair_range[0]),
                       color=COLORS['warning'], alpha=0.3, label='低估')

        # 标注当前PE
        current_y = np.exp(-0.5 * ((current_pe - mu) / sigma) ** 2)
        ax.scatter([current_pe], [current_y], s=200, color=COLORS['accent'],
                  edgecolors=COLORS['dark'], linewidths=2, zorder=5,
                  label=f'当前PE: {current_pe}')

        ax.axvline(x=current_pe, color=COLORS['accent'],
                  linestyle='--', linewidth=2, alpha=0.7)

        # 标签
        ax.text(fair_range[0], 0.1, f'低估\n<{fair_range[0]}倍',
               ha='center', fontsize=10, color=COLORS['warning'], fontfamily='sans-serif')
        ax.text(fair_range[1], 0.1, f'高估\n>{fair_range[1]}倍',
               ha='center', fontsize=10, color=COLORS['danger'], fontfamily='sans-serif')
        ax.text(mu, 0.1, f'合理\n{fair_range[0]}-{fair_range[1]}倍',
               ha='center', fontsize=10, color=COLORS['success'], fontfamily='sans-serif')

        ax.set_xlabel('市盈率 (PE)', fontsize=12, color=COLORS['dark'], fontfamily='sans-serif')
        ax.set_ylabel('概率密度', fontsize=12, color=COLORS['dark'], fontfamily='sans-serif')
        ax.legend(loc='upper right', prop={'family': 'sans-serif', 'size': 10})
        plt.title('估值区间分析', fontsize=16, fontweight='bold',
                 color=COLORS['dark'], pad=20, fontfamily='sans-serif')

        # 保存 - 使用更高DPI和质量
        if save_path is None:
            save_path = self.output_dir / 'valuation_bell_curve.png'
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'], edgecolor='none',
                   pil_kwargs={'optimize': True})
        plt.close()

        return str(save_path)

    # ========================================
    # 15. 估值对比条形图
    # ========================================
    def create_valuation_comparison(self, comparisons, current_pe, save_path=None):
        """
        创建估值对比条形图

        Args:
            comparisons: [{'name': '公司名', 'pe': 市盈率}, ...]
            current_pe: 当前公司PE
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        fig, ax = plt.subplots(figsize=self._get_figsize('medium'))
        fig.patch.set_facecolor(COLORS['background'])

        names = [c['name'] for c in comparisons]
        pes = [c['pe'] for c in comparisons]

        # 绘制条形图
        colors = [COLORS['primary']] * len(comparisons)
        if '当前公司' in names:
            idx = names.index('当前公司')
            colors[idx] = COLORS['accent']

        bars = ax.barh(names, pes, color=colors, edgecolor=COLORS['dark'],
                      linewidth=1.5, alpha=0.8)

        # 数值标签
        for bar, pe in zip(bars, pes):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                   f'{pe:.1f}倍', va='center', fontsize=10,
                   color=COLORS['dark'], fontweight='bold', fontfamily='sans-serif')

        ax.set_xlabel('市盈率 (PE)', fontsize=12, color=COLORS['dark'], fontfamily='sans-serif')
        ax.axvline(x=current_pe, color=COLORS['accent'],
                  linestyle='--', linewidth=2, alpha=0.7)
        plt.title('估值对比分析', fontsize=16, fontweight='bold',
                 color=COLORS['dark'], pad=20, fontfamily='sans-serif')

        # 保存
        if save_path is None:
            save_path = self.output_dir / 'valuation_comparison.png'
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor=COLORS['background'])
        plt.close()

        return str(save_path)


# ========================================
# 测试代码
# ========================================
if __name__ == '__main__':
    generator = StockChartGenerator()

    # 测试雷达图
    scores = {
        '业务阶段': 85,
        '护城河': 90,
        '财务健康': 85,
        '增长潜力': 65,
        '风险控制': 60
    }
    print("生成投资评分雷达图...")
    generator.create_investment_radar(scores)
    print("✅ 完成!")
