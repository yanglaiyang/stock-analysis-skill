#!/usr/bin/env python3
"""
洋河股份增强版分析脚本
使用图表可视化和金字塔原理生成专业报告
"""

import sys
import argparse
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_report_generator import EnhancedReportGenerator


def prepare_analysis_data():
    """
    准备分析数据（从Subagent输出中提取）

    这里使用洋河股份的示例数据
    实际使用时应该从Subagent分析结果中提取
    """
    company_info = {
        'name': '洋河股份',
        'code': '002304.SZ'
    }

    analysis_data = {
        # 投资评分
        'investment_scores': {
            '业务阶段': 85,
            '护城河': 90,
            '财务健康': 85,
            '增长潜力': 65,
            '风险控制': 60
        },

        # 财务指标
        'financial_metrics': {
            '营业收入': {'value': '180.90', 'unit': '亿元', 'trend': '→'},
            '毛利率': {'value': '71.10', 'unit': '%', 'trend': '→'},
            '净利率': {'value': '21.90', 'unit': '%', 'trend': '→'},
            'ROE': {'value': '7.94', 'unit': '%', 'trend': '→'},
            'PE': {'value': '12.46', 'unit': '倍', 'trend': '↓'},
            'PB': {'value': '1.71', 'unit': '倍', 'trend': '→'},
        },

        # 业务阶段
        'business_stage': {
            'current': '成熟期',
            'stages': [
                {'name': '萌芽期', 'desc': '初创阶段'},
                {'name': '成长期', 'desc': '快速发展'},
                {'name': '成熟期', 'desc': '稳定盈利'},
                {'name': '转型期', 'desc': '寻求突破'}
            ],
            'conclusion': '公司处于成熟期，是典型的"现金牛"企业'
        },

        # 商业画布
        'business_canvas': {
            'key_partners': ['经销商', '供应商', '渠道商'],
            'key_activities': ['白酒酿造', '品牌建设', '渠道管理'],
            'key_resources': ['品牌', '酿造工艺', '销售网络'],
            'value_propositions': ['绵柔型口感', '品牌文化', '产品质量'],
            'customer_relationships': ['品牌忠诚', '会员体系', '服务体验'],
            'channels': ['线下经销', '电商渠道', '餐饮渠道'],
            'customer_segments': ['个人消费', '企业客户', '经销商'],
            'cost_structure': ['原材料成本', '营销费用', '渠道费用'],
            'revenue_streams': ['白酒销售']
        },

        # 产品矩阵
        'product_portfolio': [
            {'name': '梦之蓝', 'x': 0.8, 'y': 0.8, 'size': 100},
            {'name': '天之蓝', 'x': 0.6, 'y': 0.5, 'size': 80},
            {'name': '海之蓝', 'x': 0.4, 'y': 0.3, 'size': 60}
        ],

        # 护城河评分
        'moat_scores': {
            '品牌价值': 95,
            '规模效应': 85,
            '转换成本': 60,
            '网络效应': 20,
            '成本优势': 80
        },

        # 护城河构成
        'moat_components': [
            {'name': '品牌资产', 'value': 45},
            {'name': '规模优势', 'value': 30},
            {'name': '成本优势', 'value': 20},
            {'name': '其他', 'value': 5}
        ],

        # 财务热力图（需要pandas DataFrame）
        'financial_heatmap': [
            [85, 90, 80, 75],
            [95, 90, 85, 80],
            [70, 65, 75, 70],
            [60, 65, 70, 65],
            [65, 60, 65, 60]
        ],

        # 杜邦分析
        'dupont_data': {
            'roe': 7.94,
            'net_margin': 21.90,
            'asset_turnover': 0.36,
            'equity_multiplier': 1.22,
            'gross_margin': 71.10,
            'expense_ratio': 49.20
        },

        # 现金流
        'cashflow_data': {
            'stages': [
                {'name': '营业收入', 'value': 180.90},
                {'name': '毛利润', 'value': 128.66, 'components': [128.66]},
                {'name': '净利润', 'value': 39.63, 'components': [39.63]}
            ]
        },

        # 增长驱动力
        'growth_drivers': {
            'level1': [
                {
                    'name': '获取新客户\n30%',
                    'percentage': '30%',
                    'factors': [
                        {'name': '市场投入'},
                        {'name': '新渠道'},
                        {'name': '地域扩张'}
                    ]
                },
                {
                    'name': '提升价值\n50%',
                    'percentage': '50%',
                    'factors': [
                        {'name': '定价权'},
                        {'name': '新产品'},
                        {'name': '客户留存'}
                    ]
                },
                {
                    'name': '业务创新\n20%',
                    'percentage': '20%',
                    'factors': [
                        {'name': '产品升级'},
                        {'name': '渠道创新'},
                        {'name': '数字化转型'}
                    ]
                }
            ]
        },

        # 增长阶段
        'growth_stages': {
            'current': 'mature',
            'stages': [
                {'name': 'startup'},
                {'name': 'growth'},
                {'name': 'mature'},
                {'name': 'decline'}
            ]
        },

        # 风险
        'risks': [
            {'name': '集中度风险', 'impact': 3, 'probability': 2},
            {'name': '政策风险', 'impact': 3, 'probability': 2},
            {'name': '竞争风险', 'impact': 3, 'probability': 3},
            {'name': '消费偏好变化', 'impact': 2, 'probability': 2}
        ],

        # 估值
        'valuation': {
            'current_pe': 12.46,
            'fair_range': (10, 15)
        },

        # 估值对比
        'valuation_comparison': {
            'companies': [
                {'name': '茅台', 'pe': 30},
                {'name': '五粮液', 'pe': 25},
                {'name': '洋河', 'pe': 12.46},
                {'name': '泸州老窖', 'pe': 20},
                {'name': '行业平均', 'pe': 22}
            ],
            'current_pe': 12.46
        },

        # 投资建议
        'target_price': '180-200',
        'stop_loss': '120',
        'holding_period': '12-24',

        # 各部分摘要
        'business_phase': {
            'summary': '成熟期现金牛，盈利能力强'
        },
        'moat_analysis': {
            'summary': '品牌壁垒高，护城河宽阔'
        },
        'financial_health': {
            'summary': '盈利优质，负债极低'
        },
        'growth_potential': {
            'summary': '稳健但不暴增，依赖消费升级'
        },
        'risk_assessment': {
            'summary': '行业竞争激烈，政策风险高'
        }
    }

    return company_info, analysis_data


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='洋河股份增强版分析')
    parser.add_argument('-o', '--output', default='both',
                       choices=['markdown', 'pdf', 'both'],
                       help='输出格式 (默认: both)')
    parser.add_argument('--output-dir', default='output',
                       help='输出目录 (默认: output)')

    args = parser.parse_args()

    print("=" * 60)
    print("📊 洋河股份增强版分析报告生成器")
    print("=" * 60)
    print()

    # 准备数据
    print("准备分析数据...")
    company_info, analysis_data = prepare_analysis_data()

    # 创建报告生成器
    generator = EnhancedReportGenerator(output_dir=args.output_dir)

    # 生成报告
    try:
        result = generator.generate_report(
            company_info=company_info,
            analysis_data=analysis_data,
            output_format=args.output
        )

        print()
        print("=" * 60)
        print("✅ 报告生成成功！")
        print("=" * 60)
        print()
        print(f"📄 Markdown报告: {result['markdown']}")
        if result['pdf']:
            print(f"📑 PDF报告: {result['pdf']}")
        print(f"📊 图表目录: {generator.charts_dir}")
        print()
        print("提示: 使用支持Markdown的阅读器查看.md文件")
        print("     或使用PDF阅读器查看.pdf文件")

    except Exception as e:
        print()
        print("=" * 60)
        print("❌ 报告生成失败")
        print("=" * 60)
        print()
        print(f"错误信息: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
