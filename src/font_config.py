"""
字体配置模块
自动检测和配置中文字体，支持跨平台
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import warnings


class FontConfig:
    """字体配置器 - 自动检测可用中文字体"""

    # 按优先级排列的中文字体列表
    CHINESE_FONTS = {
        'Darwin': [  # macOS
            'Arial Unicode MS',
            'PingFang SC',
            'Hiragino Sans GB',
            'STHeiti',
            'Heiti TC',
            'Microsoft YaHei',
            'SimHei',
        ],
        'Windows': [  # Windows
            'Microsoft YaHei',
            'SimHei',
            'SimSun',
            'KaiTi',
            'FangSong',
            'Arial Unicode MS',
        ],
        'Linux': [  # Linux
            'WenQuanYi Micro Hei',
            'WenQuanYi Zen Hei',
            'Noto Sans CJK SC',
            'Droid Sans Fallback',
            'AR PL UMing CN',
            'AR PL UKai CN',
            'ZCOOL QingKe HuangYou',
            'Microsoft YaHei',
            'SimHei',
        ]
    }

    FALLBACK_FONTS = [
        'DejaVu Sans',
        'Liberation Sans',
        'Arial',
    ]

    def __init__(self):
        """初始化字体配置"""
        self.system = platform.system()
        self.available_chinese_font = None
        self.font_path = None
        self._detect_chinese_font()

    def _get_available_fonts(self):
        """获取系统所有可用字体"""
        try:
            return [f.name for f in fm.fontManager.ttflist]
        except Exception as e:
            warnings.warn(f"获取字体列表失败: {e}")
            return []

    def _detect_chinese_font(self):
        """检测可用的中文字体"""
        available_fonts = self._get_available_fonts()

        # 获取对应平台的字体列表
        font_list = self.CHINESE_FONTS.get(
            self.system,
            self.CHINESE_FONTS['Linux']  # 默认使用Linux字体列表
        )

        # 尝试找到可用的中文字体
        for font in font_list:
            if font in available_fonts:
                try:
                    font_path = fm.findfont(font, fallback_to_default=False)
                    if font_path:
                        fm.fontManager.addfont(font_path)
                        self.font_path = font_path
                        self.available_chinese_font = fm.FontProperties(fname=font_path).get_name()
                        print(f"✓ 检测到中文字体: {self.available_chinese_font}")
                        return
                except Exception:
                    self.available_chinese_font = font
                    print(f"✓ 检测到中文字体: {font}")
                    return

        # 如果没有找到中文字体，使用回退字体
        for font in self.FALLBACK_FONTS:
            if font in available_fonts:
                try:
                    font_path = fm.findfont(font, fallback_to_default=False)
                    if font_path:
                        fm.fontManager.addfont(font_path)
                        self.font_path = font_path
                        self.available_chinese_font = fm.FontProperties(fname=font_path).get_name()
                        print(f"⚠ 未找到中文字体，使用回退字体: {self.available_chinese_font}")
                        print("  提示: 中文可能显示为方块，建议安装中文字体")
                        return
                except Exception:
                    self.available_chinese_font = font
                    print(f"⚠ 未找到中文字体，使用回退字体: {font}")
                    print("  提示: 中文可能显示为方块，建议安装中文字体")
                    return

        # 完全没有可用字体
        print("❌ 无法检测到任何可用字体！")
        print("  请安装系统字体包：")
        if self.system == 'Linux':
            print("  - Ubuntu/Debian: sudo apt-get install fonts-wqy-microhei fonts-noto-cjk")
            print("  - CentOS/RHEL: sudo yum install wqy-microhei-fonts")
        elif self.system == 'Darwin':
            print("  - macOS系统自带中文字体，如果出现问题请更新系统")
        elif self.system == 'Windows':
            print("  - Windows系统自带中文字体，如果出现问题请检查字体设置")

    def configure_matplotlib(self):
        """配置matplotlib使用中文字体"""
        if self.available_chinese_font:
            # 配置字体
            plt.rcParams['font.sans-serif'] = [self.available_chinese_font] + self.FALLBACK_FONTS
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
            plt.rcParams['font.family'] = 'sans-serif'

            # 打印配置信息
            print(f"✓ matplotlib已配置字体: {plt.rcParams['font.sans-serif'][0]}")
        else:
            print("⚠ 使用matplotlib默认字体配置")

        # 设置后端（无GUI环境）
        self._configure_backend()

    def _configure_backend(self):
        """配置matplotlib后端"""
        import matplotlib
        current_backend = matplotlib.get_backend()

        # 如果不是Agg后端，尝试设置为Agg（无GUI后端）
        if current_backend != 'Agg':
            try:
                matplotlib.use('Agg', force=False)
                print(f"✓ matplotlib后端: {matplotlib.get_backend()}")
            except Exception as e:
                print(f"⚠ 无法设置matplotlib后端: {e}")

    def get_font_name(self):
        """获取当前配置的字体名称"""
        return self.available_chinese_font or 'Default'

    def test_chinese_display(self):
        """测试中文显示"""
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            from pathlib import Path

            # 创建测试图
            fig, ax = plt.subplots(figsize=(8, 6))
            x = np.linspace(0, 2*np.pi, 100)
            ax.plot(x, np.sin(x))

            ax.set_title('中文显示测试 - 投资评分仪表盘', fontsize=14)
            ax.set_xlabel('横轴标签', fontsize=12)
            ax.set_ylabel('纵轴标签', fontsize=12)
            ax.text(0.5, 0.5, '测试文字: 护城河、市盈率、ROE',
                   transform=ax.transAxes, ha='center', fontsize=12)
            ax.grid(True, alpha=0.3)

            # 保存测试图
            output_dir = Path('output/charts')
            output_dir.mkdir(parents=True, exist_ok=True)
            test_path = output_dir / 'font_test.png'

            plt.savefig(test_path, dpi=150, bbox_inches='tight')
            plt.close()

            print(f"✓ 字体测试图已保存: {test_path}")
            print("  请打开图片确认中文是否正常显示")
            return True

        except Exception as e:
            print(f"✗ 字体测试失败: {e}")
            return False


# 全局字体配置实例
_font_config = None


def get_font_config():
    """获取全局字体配置实例"""
    global _font_config
    if _font_config is None:
        _font_config = FontConfig()
        _font_config.configure_matplotlib()
    return _font_config


def configure_chinese_font():
    """快捷配置中文字体"""
    get_font_config()


if __name__ == '__main__':
    print("="*60)
    print("字体配置测试")
    print("="*60)

    # 创建字体配置器
    font_config = FontConfig()

    # 配置matplotlib
    font_config.configure_matplotlib()

    # 测试中文显示
    print("\n运行中文显示测试...")
    font_config.test_chinese_display()

    print("\n字体名称:", font_config.get_font_name())
