#!/usr/bin/env python3
"""
Tushare MCP 工具客户端
直接调用 Tushare MCP 的工具函数，无需启动 MCP 服务器
"""

import sys
from pathlib import Path

# 添加 Tushare MCP 路径
TUSHARE_MCP_PATH = Path("/Users/yang/ai_coding/stock_tushare/tushare_MCP")
sys.path.insert(0, str(TUSHARE_MCP_PATH))

import tushare as ts
from config.token_manager import get_tushare_token
from cache.cache_manager import cache_manager


class DataSourceError(Exception):
    """数据源错误"""
    pass


class TushareMCPClient:
    """Tushare MCP 客户端"""

    def __init__(self):
        """初始化客户端"""
        self.token = get_tushare_token()
        if self.token:
            # 避免使用 ts.set_token(self.token) 以防止尝试写入本地文件导致权限错误
            self.pro = ts.pro_api(self.token)
            print("✅ Tushare MCP 客户端初始化成功")
        else:
            self.pro = None
            print("⚠️  未配置 Tushare token")

    def _check_client(self):
        """检查客户端是否可用"""
        if not self.pro:
            raise DataSourceError("Tushare 未配置")

    def get_stock_basic(self, ts_code: str = "", name: str = "") -> str:
        """获取股票基本信息"""
        try:
            self._check_client()
            filters = {}
            if ts_code:
                filters['ts_code'] = ts_code
            if name:
                filters['name'] = name

            df = self.pro.stock_basic(**filters)

            if df.empty:
                return f"未找到股票: {ts_code or name}"

            row = df.iloc[0]
            return f"""
### 基本信息
- 股票代码: {row['ts_code']}
- 股票名称: {row['name']}
- 所属行业: {row.get('industry', 'N/A')}
- 所属地区: {row.get('area', 'N/A')}
- 市场类型: {row.get('market', 'N/A')}
- 上市日期: {row.get('list_date', 'N/A')}
"""
        except Exception as e:
            return f"获取基本信息失败: {e}"

    def get_daily_basic(self, ts_code: str, limit: int = 1) -> str:
        """获取每日指标"""
        try:
            self._check_client()
            df = self.pro.daily_basic(ts_code=ts_code, limit=limit)

            if df.empty:
                return f"未找到每日指标数据: {ts_code}"

            latest = df.iloc[0]
            return f"""
### 每日指标 (最新)
- 交易日期: {latest['trade_date']}
- 市盈率(PE): {latest['pe']:.2f}
- 市净率(PB): {latest['pb']:.2f}
- 市销率(PS): {latest['ps']:.2f}
- 总市值: {latest['total_mv']:.2f} 亿元
- 流通市值: {latest['circ_mv']:.2f} 亿元
- 换手率: {latest['turnover_rate']:.2f}%
"""
        except Exception as e:
            return f"获取每日指标失败: {e}"

    def get_daily_quote(self, ts_code: str, limit: int = 5) -> str:
        """获取日线行情"""
        try:
            self._check_client()
            df = self.pro.daily(ts_code=ts_code, limit=limit)

            if df.empty:
                return f"未找到行情数据: {ts_code}"

            lines = ["### 日线行情 (最近5天)", ""]
            for _, row in df.head(5).iterrows():
                change_pct = ((row['close'] - row['open']) / row['open'] * 100)
                lines.append(f"""
**{row['trade_date']}**
- 开盘: {row['open']:.2f}
- 收盘: {row['close']:.2f}
- 最高: {row['high']:.2f}
- 最低: {row['low']:.2f}
- 涨跌幅: {change_pct:+.2f}%
- 成交量: {row['vol']:.0f} 手
- 成交额: {row['amount']:.2f} 千元
""")

            return "\n".join(lines)
        except Exception as e:
            return f"获取日线行情失败: {e}"

    def get_income_statement(self, ts_code: str, period: str = "") -> str:
        """获取利润表"""
        try:
            self._check_client()
            params = {'ts_code': ts_code, 'limit': 1}
            if period:
                params['period'] = period

            df = self.pro.income(**params)

            if df.empty:
                return f"未找到利润表数据: {ts_code}"

            row = df.iloc[0]
            return f"""
### 利润表 (截至 {row['end_date']})
- 营业收入: {row['total_revenue'] / 100000000:.2f} 亿元
- 营业成本: {row['oper_cost'] / 100000000 if row['oper_cost'] else 0:.2f} 亿元
- 营业利润: {row['operate_profit'] / 100000000 if row['operate_profit'] else 0:.2f} 亿元
- 利润总额: {row['total_profit'] / 100000000 if row['total_profit'] else 0:.2f} 亿元
- 净利润: {row['n_income'] / 100000000 if row['n_income'] else 0:.2f} 亿元
- 基本每股收益: {row['basic_eps']:.2f} 元
- 稀释每股收益: {row['diluted_eps']:.2f} 元
"""
        except Exception as e:
            return f"获取利润表失败: {e}"

    def get_financial_indicators(self, ts_code: str, start_date: str = "", end_date: str = "") -> str:
        """获取财务指标"""
        try:
            self._check_client()
            params = {'ts_code': ts_code, 'limit': 1}
            if start_date:
                params['start_date'] = start_date
            if end_date:
                params['end_date'] = end_date

            df = self.pro.fina_indicator(**params)

            if df.empty:
                return f"未找到财务指标数据: {ts_code}"

            row = df.iloc[0]
            return f"""
### 财务指标 (截至 {row['end_date']})
- ROE(净资产收益率): {row['roe']:.2f}%
- ROA(总资产净利率): {row['roa']:.2f}%
- 毛利率: {row['grossprofit_margin']:.2f}%
- 净利率: {row['netprofit_margin']:.2f}%
- 资产负债率: {row['debt_to_assets']:.2f}%
- 流动比率: {row['current_ratio']:.2f}
- 速动比率: {row['quick_ratio']:.2f}
-每股净资产: {row['bps']:.2f} 元
"""
        except Exception as e:
            return f"获取财务指标失败: {e}"

    def get_all_data(self, ts_code: str) -> str:
        """获取所有分析数据"""
        parts = []

        # 1. 基本信息
        basic = self.get_stock_basic(ts_code=ts_code)
        if basic:
            parts.append(basic)

        # 2. 每日指标
        daily_basic = self.get_daily_basic(ts_code)
        if daily_basic:
            parts.append(daily_basic)

        # 3. 日线行情
        daily = self.get_daily_quote(ts_code)
        if daily:
            parts.append(daily)

        # 4. 利润表
        income = self.get_income_statement(ts_code)
        if income:
            parts.append(income)

        # 5. 财务指标
        indicators = self.get_financial_indicators(ts_code)
        if indicators:
            parts.append(indicators)

        return "\n".join(parts)


# 创建全局客户端实例
_tushare_client = None

def get_tushare_client():
    """获取 Tushare MCP 客户端实例"""
    global _tushare_client
    if _tushare_client is None:
        _tushare_client = TushareMCPClient()
    return _tushare_client
