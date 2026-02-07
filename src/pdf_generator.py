"""
PDF报告生成器
将Markdown报告和图表整合为专业PDF文档

特性：
- 支持Markdown转PDF
- 嵌入高清图表
- 蓝色商务风样式
- 自动分页和目录
- 中文字体支持
"""

import os
import sys
import base64
import re
from pathlib import Path
from datetime import datetime

# 抑制weasyprint的警告
import warnings
warnings.filterwarnings('ignore')

try:
    from weasyprint import HTML, CSS
    from jinja2 import Template
    PDF_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ PDF生成功能不可用: {e}")
    print("   请安装: pip install weasyprint jinja2")
    PDF_AVAILABLE = False


class PDFReportGenerator:
    """PDF报告生成器"""

    def __init__(self, output_dir='reports'):
        """
        初始化PDF报告生成器

        Args:
            output_dir: 报告输出目录
        """
        if not PDF_AVAILABLE:
            raise RuntimeError("PDF生成功能不可用，请安装weasyprint和jinja2")

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 检测中文字体
        self.chinese_fonts = self._detect_chinese_fonts()

    def _detect_chinese_fonts(self):
        """检测系统中可用的中文字体"""
        font_families = []

        # macOS字体
        font_families.extend([
            'PingFang SC',
            'Hiragino Sans GB',
            'STHeiti',
            'Arial Unicode MS'
        ])

        # Windows字体
        font_families.extend([
            'Microsoft YaHei',
            'SimHei',
            'SimSun'
        ])

        # Linux字体
        font_families.extend([
            'WenQuanYi Micro Hei',
            'Noto Sans CJK SC',
            'WenQuanYi Zen Hei'
        ])

        return font_families

    def _image_to_base64(self, image_path: str) -> str:
        """将图片转换为Base64字符串"""
        if not image_path:
            return ""

        image_path = Path(image_path)
        if not image_path.exists():
            return ""

        try:
            with open(image_path, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode("utf-8")

            ext = image_path.suffix.lower()
            mime_type = "image/png" if ext == ".png" else "image/jpeg"
            return f"data:{mime_type};base64,{encoded_string}"
        except Exception:
            return ""

    def _resolve_image_path(self, src: str, output_path: str, chart_paths: list) -> Path:
        """解析图片路径（支持相对路径和chart_paths匹配）"""
        if not src:
            return None

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

        if chart_paths:
            for p in chart_paths:
                if not p:
                    continue
                p = Path(p)
                if p == src_path or p.name == src_path.name:
                    candidates.append(p)

        for c in candidates:
            if c.exists():
                return c
        return None

    def _embed_local_images_in_html(self, html_body: str, output_path: str, chart_paths: list) -> str:
        """将HTML中的本地图片路径转换为Base64，确保PDF内嵌"""
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

    def _create_html_template(self):
        """创建HTML模板（使用蓝色商务风样式和中文字体支持）"""
        # 构建中文字体栈
        font_stack = ', '.join(self.chinese_fonts)
        font_family = "'Helvetica Neue', Arial, " + font_stack + ", sans-serif"

        # 使用 .format() 而不是 f-string 来避免大括号转义问题
        template_str = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{{{{ title }}}}</title>
    <style>
        /* 全局样式 */
        @page {{
            size: A4;
            margin: 2cm;
            @bottom-center {{
                content: "第 " counter(page) " 页 / 共 " counter(pages) " 页";
                font-size: 10pt;
                color: #95a5a6;
            }}
        }}

        body {{
            font-family: {FONT_FAMILY};
            line-height: 1.6;
            color: #2c3e50;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
        }}

        /* 标题样式 */
        h1 {{
            color: #1a5276;
            font-size: 28pt;
            font-weight: bold;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
            margin-bottom: 20px;
            page-break-after: avoid;
        }}

        h2 {{
            color: #1f77b4;
            font-size: 22pt;
            font-weight: bold;
            border-left: 5px solid #3498db;
            padding-left: 15px;
            margin-top: 30px;
            margin-bottom: 15px;
            page-break-after: avoid;
        }}

        h3 {{
            color: #3498db;
            font-size: 18pt;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            page-break-after: avoid;
        }}

        h4 {{
            color: #5dade2;
            font-size: 14pt;
            font-weight: bold;
            margin-top: 15px;
            margin-bottom: 8px;
            page-break-after: avoid;
        }}

        /* 段落和文本 */
        p {{
            margin: 10px 0;
            text-align: justify;
        }}

        strong {{
            color: #1a5276;
            font-weight: bold;
        }}

        /* 列表 */
        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}

        li {{
            margin: 5px 0;
        }}

        /* 表格样式 */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 10pt;
        }}

        thead {{
            background-color: #1f77b4;
            color: white;
        }}

        th {{
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #1a5276;
        }}

        td {{
            padding: 10px;
            border: 1px solid #d5dbdb;
        }}

        tbody tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}

        tbody tr:hover {{
            background-color: #eaf2f8;
        }}

        /* 代码块 */
        pre {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'SFMono-Regular', 'Menlo', 'Consolas', {FONT_FAMILY}, monospace;
            font-size: 9pt;
        }}

        code {{
            background-color: #eaf2f8;
            color: #1a5276;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'SFMono-Regular', 'Menlo', 'Consolas', {FONT_FAMILY}, monospace;
            font-size: 9pt;
        }}

        /* 引用块 */
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin: 15px 0;
            color: #7f8c8d;
            font-style: italic;
            background-color: #f8f9fa;
            padding: 15px;
        }}

        /* 图片 */
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .chart-container {{
            text-align: center;
            margin: 30px 0;
            page-break-inside: avoid;
        }}

        .chart-container img {{
            display: inline-block;
            margin: 10px auto;
        }}

        .chart-caption {{
            font-size: 10pt;
            color: #7f8c8d;
            text-align: center;
            margin-top: 10px;
            font-style: italic;
        }}

        /* 分隔线 */
        hr {{
            border: none;
            border-top: 2px solid #d5dbdb;
            margin: 30px 0;
        }}

        /* 信息框 */
        .info-box {{
            background-color: #eaf2f8;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
        }}

        .warning-box {{
            background-color: #fef5e7;
            border-left: 4px solid #f39c12;
            padding: 15px;
            margin: 20px 0;
        }}

        .danger-box {{
            background-color: #fadbd8;
            border-left: 4px solid #e74c3c;
            padding: 15px;
            margin: 20px 0;
        }}

        .success-box {{
            background-color: #d5f4e6;
            border-left: 4px solid #27ae60;
            padding: 15px;
            margin: 20px 0;
        }}

        /* 徽章 */
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 8pt;
            font-weight: bold;
            color: white;
        }}

        .badge-success {{ background-color: #27ae60; }}
        .badge-warning {{ background-color: #f39c12; }}
        .badge-danger {{ background-color: #e74c3c; }}
        .badge-primary {{ background-color: #3498db; }}
        .badge-neutral {{ background-color: #95a5a6; }}

        /* 卡片 */
        .card {{
            background-color: white;
            border: 1px solid #d5dbdb;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        .card-title {{
            font-size: 16pt;
            font-weight: bold;
            color: #1a5276;
            margin-bottom: 15px;
        }}

        /* 网格布局 */
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }}

        .grid-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }}

        /* 指标卡片 */
        .metric-card {{
            background: linear-gradient(135deg, #1f77b4 0%, #3498db 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .metric-value {{
            font-size: 24pt;
            font-weight: bold;
            margin: 10px 0;
        }}

        .metric-label {{
            font-size: 10pt;
            opacity: 0.9;
        }}

        .metric-trend {{
            font-size: 14pt;
            margin-top: 5px;
        }}

        /* 页面分割 */
        .page-break {{
            page-break-after: always;
        }}

        .no-break {{
            page-break-inside: avoid;
        }}

        /* 目录 */
        .toc {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}

        .toc h2 {{
            margin-top: 0;
            border-bottom: 2px solid #3498db;
        }}

        .toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}

        .toc li {{
            margin: 8px 0;
        }}

        .toc a {{
            color: #1f77b4;
            text-decoration: none;
        }}

        .toc a:hover {{
            text-decoration: underline;
        }}

        /* 执行摘要 */
        .executive-summary {{
            background: linear-gradient(135deg, #eaf2f8 0%, #d6eaf8 100%);
            padding: 25px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 5px solid #1f77b4;
        }}

        /* 投资建议 */
        .investment-recommendation {{
            background-color: #27ae60;
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin: 20px 0;
        }}

        .investment-recommendation h3 {{
            color: white;
            margin: 0;
        }}

        /* 风险等级 */
        .risk-high {{
            color: #e74c3c;
            font-weight: bold;
        }}

        .risk-medium {{
            color: #f39c12;
            font-weight: bold;
        }}

        .risk-low {{
            color: #27ae60;
            font-weight: bold;
        }}

        /* 免责声明 */
        .disclaimer {{
            font-size: 8pt;
            color: #95a5a6;
            text-align: center;
            padding: 20px;
            border-top: 1px solid #d5dbdb;
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    {{{{ content }}}}
</body>
</html>
        '''

        return Template(template_str.replace('{FONT_FAMILY}', font_family))

    def markdown_to_html(self, markdown_content):
        """
        将Markdown转换为HTML（简化版）

        Args:
            markdown_content: Markdown内容

        Returns:
            HTML内容
        """
        html = markdown_content

        # 标题
        html = html.replace('# ', '<h1>').replace('\n', '</h1>\n', 1)
        html = html.replace('## ', '<h2>').replace('\n', '</h2>\n', 1)
        html = html.replace('### ', '<h3>').replace('\n', '</h3>\n', 1)

        # 粗体
        html = html.replace('**', '<strong>', 1).replace('**', '</strong>', 1)

        # 图片（图表）
        import re
        html = re.sub(r'!\[(.*?)\]\((.*?)\)',
                     r'<div class="chart-container"><img src="\2" alt="\1"><p class="chart-caption">\1</p></div>',
                     html)

        # 链接
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)

        # 表格（简化处理）
        # 这里只处理简单表格，复杂表格建议使用pandoc

        # 段落
        lines = html.split('\n')
        result_lines = []
        in_paragraph = False

        for line in lines:
            if line.strip() == '':
                if in_paragraph:
                    result_lines.append('</p>')
                    in_paragraph = False
            elif line.startswith('#') or line.startswith('<h') or line.startswith('<div'):
                if in_paragraph:
                    result_lines.append('</p>')
                    in_paragraph = False
                result_lines.append(line)
            elif line.startswith('```'):
                # 代码块
                if in_paragraph:
                    result_lines.append('</p>')
                    in_paragraph = False
                result_lines.append(line)
            else:
                if not in_paragraph:
                    result_lines.append('<p>')
                    in_paragraph = True
                result_lines.append(line)

        if in_paragraph:
            result_lines.append('</p>')

        html = '\n'.join(result_lines)

        return html

    def generate_pdf(self, markdown_content, title, output_filename=None, chart_paths=None):
        """
        生成PDF报告

        Args:
            markdown_content: Markdown格式报告内容
            title: 报告标题
            output_filename: 输出文件名（可选）

        Returns:
            PDF文件路径
        """
        # 转换为HTML
        html_content = self.markdown_to_html(markdown_content)

        # 使用模板
        template = self._create_html_template()
        full_html = template.render(title=title, content=html_content)

        # 确定输出路径
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f'stock_analysis_report_{timestamp}.pdf'

        output_path = self.output_dir / output_filename

        # 嵌入本地图片为Base64，确保PDF可显示图表
        full_html = self._embed_local_images_in_html(full_html, str(output_path), chart_paths=chart_paths or [])

        # 生成PDF
        print(f"正在生成PDF报告: {output_path}")
        HTML(string=full_html).write_pdf(
            output_path,
            stylesheets=None,
            presentational_hints=True
        )
        print(f"✅ PDF报告已保存至: {output_path}")

        return str(output_path)

    def generate_pdf_with_charts(self, markdown_content, title, chart_paths, output_filename=None):
        """
        生成带图表的PDF报告

        Args:
            markdown_content: Markdown格式报告内容
            title: 报告标题
            chart_paths: 图表路径列表
            output_filename: 输出文件名（可选）

        Returns:
            PDF文件路径
        """
        # 转换Markdown中的图表占位符为实际图片标签
        import re

        # 假设图表占位符格式为: ![图表名称](chart:filename)
        def replace_chart_placeholder(match):
            chart_name = match.group(1)
            chart_filename = match.group(2).replace('chart:', '')

            # 查找对应的图表路径
            for chart_path in chart_paths:
                if chart_filename in str(chart_path):
                    return f'<div class="chart-container"><img src="{chart_path}" alt="{chart_name}"><p class="chart-caption">{chart_name}</p></div>'

            # 如果找不到，返回占位符
            return match.group(0)

        # 替换图表占位符
        markdown_content = re.sub(r'!\[(.*?)\]\(chart:(.*?)\)', replace_chart_placeholder, markdown_content)

        # 生成PDF
        if isinstance(chart_paths, dict):
            resolved_paths = list(chart_paths.values())
        elif isinstance(chart_paths, (list, tuple)):
            resolved_paths = list(chart_paths)
        else:
            resolved_paths = []

        return self.generate_pdf(markdown_content, title, output_filename, chart_paths=resolved_paths)


# 测试代码
if __name__ == '__main__':
    generator = PDFReportGenerator()

    # 测试内容
    test_markdown = """
# 洋河股份投资分析报告

## 执行摘要

这是一份测试报告，展示PDF生成功能。

### 投资评级

![投资评分雷达图](chart:investment_radar.png)

### 核心数据

| 指标 | 数值 | 评级 |
|------|------|------|
| 毛利率 | 71.10% | 优秀 |
| 净利率 | 21.90% | 优秀 |
| ROE | 7.94% | 良好 |

## 免责声明

本报告由AI生成，仅供参考。
    """

    # 生成测试PDF（需要实际图表文件）
    print("PDF生成器模块已就绪")
    print("注意：完整功能需要配合图表文件使用")
