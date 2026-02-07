
"""
HTML报告生成器
将Markdown报告和图表整合为专业交互式HTML研报

特性：
- 蓝色商务风样式
- 嵌入Base64图片（单文件，便于分享）
- 响应式设计（适配手机/平板）
- 打印优化（支持另存为PDF）
- 中文字体完美支持
- 图表自动嵌入
"""

import os
import sys
import base64
import re
from pathlib import Path
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import markdown
    from jinja2 import Template
    MARKDOWN_AVAILABLE = True
except ImportError:
    print("⚠️ markdown 或 jinja2 未安装，使用简化模式")
    MARKDOWN_AVAILABLE = False

# 默认HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        :root {
            --primary-color: #1f77b4;
            --secondary-color: #3498db;
            --dark-color: #1a5276;
            --light-color: #85c1e9;
            --accent-color: #e74c3c;
            --success-color: #27ae60;
            --warning-color: #f39c12;
            --bg-color: #f8f9fa;
            --text-color: #2c3e50;
            --card-bg: #ffffff;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'Heiti SC', 'Arial Unicode MS', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.8;
            color: var(--text-color);
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: var(--card-bg);
            padding: 50px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            border-radius: 12px;
        }

        /* 打印控制 */
        @media print {
            body {
                background: white;
                padding: 0;
            }
            .container {
                box-shadow: none;
                max-width: 100%;
                padding: 20px;
            }
            .no-print {
                display: none !important;
            }
            a {
                text-decoration: none;
                color: black;
            }
            h1, h2, h3 {
                page-break-after: avoid;
            }
            img, .chart-container {
                page-break-inside: avoid;
            }
        }

        /* 响应式设计 - 增强版 */
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }

            h1 {
                font-size: 1.8em !important;
            }

            h2 {
                font-size: 1.4em !important;
            }

            h3 {
                font-size: 1.2em !important;
            }

            /* 表格移动端优化 */
            table {
                font-size: 0.85em;
            }

            th, td {
                padding: 8px 6px;
            }

            .table-wrapper {
                border-radius: 4px;
            }

            /* 图表移动端优化 */
            .chart-container {
                padding: 15px 10px;
                margin: 20px 0;
            }

            img {
                max-width: 100%;
                height: auto !important;
            }

            /* 徽章移动端优化 */
            .badge {
                font-size: 0.75em;
                padding: 3px 8px;
                margin: 2px;
            }

            /* 列表移动端优化 */
            ul, ol {
                padding-left: 20px;
            }

            /* 引用块移动端优化 */
            blockquote {
                padding: 15px;
                margin: 15px 0;
            }

            /* 工具栏移动端隐藏 */
            .toolbar {
                position: static;
                margin-bottom: 20px;
                justify-content: center;
            }

            .btn {
                padding: 10px 16px;
                font-size: 12px;
            }
        }

        /* 超小屏幕优化（375px及以下） */
        @media (max-width: 375px) {
            .container {
                padding: 15px;
            }

            h1 {
                font-size: 1.5em !important;
            }

            h2 {
                font-size: 1.2em !important;
                padding-left: 12px !important;
            }

            h3 {
                font-size: 1.1em !important;
            }

            table {
                font-size: 0.8em;
            }

            th, td {
                padding: 6px 4px;
            }

            .chart-caption {
                font-size: 0.85em;
            }

            p, li {
                font-size: 0.9em;
            }

            /* 隐藏非关键元素 */
            .no-mobile {
                display: none !important;
            }
        }

        /* 顶部工具栏 */
        .toolbar {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            display: flex;
            gap: 10px;
        }

        .btn {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(31, 119, 180, 0.3);
            transition: all 0.3s ease;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(31, 119, 180, 0.4);
        }

        /* 标题样式 */
        h1 {
            color: var(--dark-color);
            border-bottom: 4px solid var(--secondary-color);
            padding-bottom: 15px;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 40px;
            background: linear-gradient(135deg, var(--dark-color), var(--primary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        h2 {
            color: var(--primary-color);
            border-left: 6px solid var(--secondary-color);
            padding-left: 20px;
            margin-top: 50px;
            margin-bottom: 25px;
            background: linear-gradient(to right, #eaf2f8 0%, transparent 100%);
            padding: 15px 20px;
            border-radius: 0 8px 8px 0;
            font-size: 1.8em;
        }

        h3 {
            color: var(--secondary-color);
            margin-top: 30px;
            margin-bottom: 15px;
            font-weight: 600;
            font-size: 1.4em;
        }

        h4 {
            color: var(--dark-color);
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 1.2em;
        }

        /* 段落 */
        p {
            margin: 15px 0;
            text-align: justify;
        }

        /* 列表 */
        ul, ol {
            margin: 15px 0;
            padding-left: 30px;
        }

        li {
            margin: 8px 0;
        }

        /* 表格样式 - 优化版 */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.95em;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
            table-layout: auto;
        }

        th {
            background: linear-gradient(135deg, var(--dark-color), var(--primary-color));
            color: white;
            padding: 15px 12px;
            text-align: left;
            font-weight: 600;
            white-space: nowrap;
            position: relative;
        }

        td {
            padding: 12px;
            border-bottom: 1px solid #eee;
            word-wrap: break-word;
            max-width: 400px;
        }

        /* Safari表格边框修复 */
        @supports (-webkit-appearance: none) {
            table {
                border: 1px solid #ddd;
            }

            th, td {
                border-right: 1px solid #eee;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }

            th:last-child, td:last-child {
                border-right: none;
            }

            /* Safari图片渲染优化 */
            img {
                -webkit-backface-visibility: hidden;
                image-rendering: -webkit-optimize-contrast;
            }
        }

        /* Safari字体平滑 */
        body {
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* Safari渐变背景修复 */
        .container {
            background-attachment: scroll;
        }

        /* Safari按钮样式修复 */
        .btn {
            -webkit-appearance: none;
            border-radius: 8px;
            -webkit-font-smoothing: antialiased;
        }

        tr:nth-child(even) {
            background-color: #f8f9fa;
        }

        tr:hover {
            background-color: #eaf2f8;
        }

        /* 表格内图标和标签对齐 */
        td .badge, td strong {
            display: inline-block;
            margin: 2px 4px;
            vertical-align: middle;
        }

        /* 防止文字与图标重叠 */
        td > *:first-child {
            margin-right: 4px;
        }

        /* 表格响应式包装 */
        .table-wrapper {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .table-wrapper table {
            margin: 0;
            min-width: 600px;
        }

        /* 图片与图表 */
        .chart-container {
            text-align: center;
            margin: 40px 0;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }

        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .chart-caption {
            font-size: 0.95em;
            color: #7f8c8d;
            margin-top: 15px;
            font-weight: 500;
        }

        /* 引用块 */
        blockquote {
            background: linear-gradient(135deg, #eaf2f8 0%, #ffffff 100%);
            border-left: 5px solid var(--secondary-color);
            margin: 20px 0;
            padding: 20px;
            color: #555;
            border-radius: 0 8px 8px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        /* 代码块 */
        pre {
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'SFMono-Regular', 'Menlo', 'Consolas', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'SimHei', monospace;
            font-size: 0.9em;
            line-height: 1.6;
        }

        code {
            background-color: #eaf2f8;
            color: var(--dark-color);
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'SFMono-Regular', 'Menlo', 'Consolas', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'SimHei', monospace;
            font-size: 0.9em;
        }

        /* 强调 */
        strong {
            color: var(--primary-color);
            font-weight: 600;
        }

        /* 分隔线 */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(to right, transparent, var(--secondary-color), transparent);
            margin: 40px 0;
        }

        /* 徽章 */
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            color: white;
            font-size: 0.85em;
            font-weight: 600;
            margin: 0 5px;
        }

        .badge-success { background-color: var(--success-color); }
        .badge-warning { background-color: var(--warning-color); }
        .badge-danger { background-color: var(--accent-color); }
        .badge-primary { background-color: var(--primary-color); }
        .badge-neutral { background-color: #95a5a6; }

        /* 状态颜色 */
        .status-red { color: var(--accent-color); font-weight: bold; }
        .status-yellow { color: var(--warning-color); font-weight: bold; }
        .status-green { color: var(--success-color); font-weight: bold; }

        /* 页脚 */
        .footer {
            text-align: center;
            margin-top: 60px;
            padding: 30px;
            color: #7f8c8d;
            font-size: 0.85em;
            border-top: 2px solid #eee;
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            border-radius: 8px;
        }

        /* 链接 */
        a {
            color: var(--primary-color);
            text-decoration: none;
            border-bottom: 1px dotted var(--primary-color);
            transition: all 0.3s;
        }

        a:hover {
            color: var(--secondary-color);
            border-bottom-style: solid;
        }

        /* 投资建议框 */
        .recommendation-box {
            background: linear-gradient(135deg, var(--success-color) 0%, #229954 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            margin: 30px 0;
            box-shadow: 0 6px 20px rgba(39, 174, 96, 0.3);
        }

        .recommendation-box h3 {
            color: white;
            margin: 0;
        }
    </style>
</head>
<body>
    <div class="toolbar no-print">
        <button class="btn" onclick="window.print()">🖨️ 打印 / PDF</button>
        <button class="btn" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">⬆️ 返回顶部</button>
    </div>

    <div class="container">
        {{ content }}

        <div class="footer">
            <p><strong>AI 股票分析报告</strong></p>
            <p>生成时间: {{ timestamp }}</p>
            <p>分析方法: Subagent架构 (7个专业化AI Agent) + 可视化增强</p>
            <p style="margin-top: 15px; color: #e74c3c; font-weight: 600;">⚠️ 免责声明: 本报告由AI系统自动生成，所有分析结论仅供参考，不构成任何投资建议。股票投资有风险，决策需谨慎。</p>
        </div>
    </div>

    <script>
        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // 打印提示
        window.addEventListener('beforeprint', function() {
            console.log('准备打印报告...');
        });
    </script>
</body>
</html>
"""


class HtmlReportGenerator:
    """HTML报告生成器"""

    def __init__(self, output_dir='output'):
        """
        初始化HTML报告生成器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ HTML报告生成器已初始化，输出目录: {self.output_dir}")

    def _image_to_base64(self, image_path: str) -> str:
        """
        将图片转换为Base64字符串

        Args:
            image_path: 图片路径

        Returns:
            Base64编码的data URI
        """
        if not image_path:
            return ""

        image_path = Path(image_path)

        if not image_path.exists():
            print(f"   ⚠️ 图片文件不存在: {image_path}")
            return ""

        try:
            with open(image_path, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

            ext = image_path.suffix.lower()
            mime_type = "image/png" if ext == '.png' else "image/jpeg"

            print(f"   ✓ 图片转换成功: {image_path.name} ({len(encoded_string)//1024}KB)")
            return f"data:{mime_type};base64,{encoded_string}"

        except Exception as e:
            print(f"   ❌ 图片转换失败: {image_path}, 错误: {e}")
            return ""

    def _resolve_image_path(self, src: str, output_path: str, chart_paths: dict) -> Path:
        """
        解析图片路径（支持相对路径、输出目录、chart_paths匹配）

        Args:
            src: HTML img src
            output_path: HTML输出路径
            chart_paths: 图表路径字典

        Returns:
            存在的图片路径（或None）
        """
        if not src:
            return None

        # 已是data URI或网络资源，直接跳过
        if src.startswith("data:") or re.match(r"^https?://", src, re.IGNORECASE):
            return None

        src_path = Path(src)

        candidates = []
        if src_path.is_absolute():
            candidates.append(src_path)
        else:
            if output_path:
                candidates.append(Path(output_path).parent / src_path)
            candidates.append(Path.cwd() / src_path)

        # 尝试在chart_paths中按文件名匹配
        if chart_paths:
            for _, p in chart_paths.items():
                if not p:
                    continue
                p = Path(p)
                if p == src_path or p.name == src_path.name:
                    candidates.append(p)

        for c in candidates:
            if c.exists():
                return c

        return None

    def _embed_local_images_in_html(self, html_body: str, output_path: str, chart_paths: dict) -> str:
        """
        将HTML中的本地图片路径转换为Base64，确保可移植
        """
        img_re = re.compile(r'<img([^>]*?)src=["\']([^"\']+)["\']([^>]*)>', re.IGNORECASE)

        def _replace(match):
            src = match.group(2)
            resolved = self._resolve_image_path(src, output_path, chart_paths)
            if not resolved:
                return match.group(0)

            base64_img = self._image_to_base64(str(resolved))
            if not base64_img:
                return match.group(0)

            return f'<img{match.group(1)}src="{base64_img}"{match.group(3)}>'

        return img_re.sub(_replace, html_body)

    def generate_report(self, markdown_content: str, chart_paths: dict,
                       output_path: str = None, title: str = "股票分析报告"):
        """
        生成HTML报告

        Args:
            markdown_content: Markdown文本
            chart_paths: 图表路径字典 {'图表名称': 'path/to/image.png'}
            output_path: 输出HTML文件路径（可选）
            title: 报告标题（可选）

        Returns:
            生成的HTML文件路径
        """
        print("\n" + "="*60)
        print("📄 生成HTML报告")
        print("="*60)

        # DEBUG: 打印chart_paths的内容
        print(f"\n📊 DEBUG - chart_paths keys: {list(chart_paths.keys())}")
        for k, v in chart_paths.items():
            print(f"  '{k}' -> '{v}'")

        # 1. 先转换图表为Base64 HTML
        print(f"\n📊 准备嵌入图表...")
        embedded_charts = 0
        chart_html_map = {}

        # 图表中文名称映射
        chart_name_map = {
            'CHART_RADAR': '投资分析雷达图',
            'CHART_INVESTMENT_RADAR': '投资评分雷达图',
            'CHART_MOAT': '护城河评分雷达图',
            'CHART_FINANCIAL': '财务健康度热力图',
            'CHART_VALUATION': '估值分析图',
            'investment_radar': '投资评分雷达图',
            'financial_cards': '核心财务指标卡片',
            'business_stage': '业务阶段时间轴',
            'business_canvas': '商业模式画布',
            'product_portfolio': '产品矩阵图',
            'moat_radar': '护城河评分雷达图',
            'moat_waterfall': '护城河构成瀑布图',
            'financial_heatmap': '财务健康度热力图',
            'dupont_analysis': '杜邦分析图',
            'cashflow_sankey': '现金流桑基图',
            'growth_tree': '增长驱动力树状图',
            'growth_curve': '增长阶段曲线',
            'risk_matrix': '风险矩阵图',
            'valuation_bell': '估值钟形曲线',
            'valuation_comparison': '估值对比条形图',
        }

        for chart_name, chart_path in chart_paths.items():
            if not chart_path:
                continue

            print(f"\n处理图表: {chart_name}")
            base64_img = self._image_to_base64(chart_path)

            if base64_img:
                # 使用中文名称作为caption
                display_name = chart_name_map.get(chart_name, chart_name)
                # 生成HTML图表容器
                img_html = f'''<div class="chart-container">
    <img src="{base64_img}" alt="{display_name}">
    <p class="chart-caption">{display_name}</p>
</div>'''
                chart_html_map[chart_name] = img_html
                embedded_charts += 1

        print(f"\n✅ 成功转换 {embedded_charts} 张图表为HTML")

        # 2. 预处理 Markdown：先替换图表占位符为特殊标记
        processed_md = markdown_content

        # 创建占位符映射（从chart_paths到chart_html）
        placeholder_map = {}
        for chart_key, chart_html in chart_html_map.items():
            # 使用HTML注释作为占位符（不会被Markdown过滤）
            placeholder = f"<!--CHART_PLACEHOLDER_{chart_key}-->"
            placeholder_map[placeholder] = chart_html

            # 在Markdown中查找并替换图表占位符
            # 支持多种格式：{{CHART_XXX}} 或单独的图表名称
            import re
            # 替换 {{CHART_XXX}} 格式
            processed_md = re.sub(
                rf'{{{{{chart_key}}}}}',
                placeholder,
                processed_md
            )
            # 替换单独的图表名称行
            lines = processed_md.split('\n')
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped == chart_key or stripped == f'{{{{{chart_key}}}}}':
                    lines[i] = placeholder
            processed_md = '\n'.join(lines)

        # DEBUG: 检查占位符替换是否成功
        print(f"\n🔧 DEBUG - 检查processed_md中的占位符:")
        for placeholder in list(placeholder_map.keys()):
            if placeholder in processed_md:
                print(f"  ✓ processed_md中找到: {placeholder[:60]}")
            else:
                print(f"  ✗ processed_md中未找到: {placeholder[:60]}")

        # 3. 转换 Markdown 为 HTML
        print("\n📝 转换 Markdown 为 HTML...")

        # 预处理Markdown：确保所有表格块前都有空行
        lines = processed_md.split('\n')
        processed_lines = []
        in_table = False

        for i, line in enumerate(lines):
            is_table_line = line.strip().startswith('|')

            # 开始表格
            if is_table_line and not in_table:
                # 如果前一行不是空行，插入空行
                if i > 0 and lines[i-1].strip() != '':
                    processed_lines.append('')
                in_table = True
                processed_lines.append(line)
            # 结束表格
            elif not is_table_line and in_table:
                in_table = False
                processed_lines.append(line)
            else:
                processed_lines.append(line)

        processed_md = '\n'.join(processed_lines)

        if MARKDOWN_AVAILABLE:
            try:
                html_body = markdown.markdown(
                    processed_md,
                    extensions=['tables', 'fenced_code', 'attr_list', 'sane_lists']
                )
                print("✓ Markdown 转换成功")
            except Exception as e:
                print(f"⚠️ Markdown 转换失败: {e}，使用原始内容")
                html_body = f"<div>{processed_md}</div>"
        else:
            # 简单转换（如果没有markdown库）
            html_body = f"<div>{processed_md.replace(chr(10), '<br>')}</div>"
            print("⚠️ 使用简化HTML转换")

        # 4. 替换占位符为实际的图表HTML
        print(f"\n🔧 DEBUG - placeholder_map: {list(placeholder_map.keys())}")
        charts_embedded = 0
        for placeholder, chart_html in placeholder_map.items():
            if placeholder in html_body:
                print(f"  ✓ 找到占位符: {placeholder[:50]}...")
                html_body = html_body.replace(placeholder, chart_html)
                charts_embedded += 1
            else:
                # 尝试处理被包裹在<p>标签中的情况
                p_wrapped = f"<p>{placeholder}</p>"
                if p_wrapped in html_body:
                    print(f"  ✓ 找到包裹的占位符: {p_wrapped[:50]}...")
                    html_body = html_body.replace(p_wrapped, chart_html)
                    charts_embedded += 1
                else:
                    print(f"  ✗ 未找到占位符: {placeholder[:50]}...")

        print(f"\n✅ 成功嵌入 {charts_embedded} 张图表")

        # 4.1 尝试将Markdown图片路径转为Base64（增强兼容）
        html_body = self._embed_local_images_in_html(html_body, output_path, chart_paths)

        # 5. 渲染模板
        print("🎨 渲染HTML模板...")

        try:
            template = Template(HTML_TEMPLATE)
            final_html = template.render(
                title=title,
                content=html_body,
                timestamp=datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
            )
            print("✓ 模板渲染成功")
        except Exception as e:
            print(f"❌ 模板渲染失败: {e}")
            return None

        # 6. 确定输出路径
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.output_dir / f"股票分析报告_{timestamp}.html"
        else:
            output_path = Path(output_path)

        # 7. 保存文件
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)

            file_size = output_path.stat().st_size / 1024  # KB
            print(f"\n✅ HTML报告已生成: {output_path}")
            print(f"   文件大小: {file_size:.1f} KB")
            print(f"   嵌入图表: {embedded_charts} 张")

            return str(output_path)

        except Exception as e:
            print(f"❌ 保存HTML文件失败: {e}")
            return None


# 测试代码
if __name__ == '__main__':
    # 创建测试报告
    generator = HtmlReportGenerator()

    # 测试 Markdown 内容
    test_md = """
# 测试公司投资分析报告

## 投资评级

根据综合分析，我们给予该公司 **买入** 评级。

## 核心财务数据

| 指标 | 数值 | 评级 |
|------|------|------|
| 营业收入 | 180.90亿元 | 优秀 |
| 净利润 | 39.61亿元 | 优秀 |
| ROE | 7.94% | 良好 |

## 风险提示

> 投资有风险，入市需谨慎。本报告仅供参考，不构成投资建议。
    """

    # 生成测试报告（不包含图表）
    test_output = generator.generate_report(
        markdown_content=test_md,
        chart_paths={},
        output_path="test_report.html",
        title="测试报告"
    )

    print(f"\n测试完成: {test_output}")
