from dataclasses import dataclass
from datetime import datetime as dt
import datetime

@dataclass
class FundDomainInputDto:
    snapshot: list
    condition: any = None

@dataclass
class FundInputDto:
    fund_name: str
    start: str = None
    limit: int = None
    interval: int = None
    uid: str = None

@dataclass
class FundOutputDto:
    series: any

@dataclass
class FundPortChartDto:
    datetime :  datetime
    day_percent : float
    total_percent : float
    day_return : float
    total_qty : float
    datestr : str
    timestr : str

@dataclass
class FundAssetDto:
    fund_asset : float

@dataclass
class FundReportDto:
    datetime : datetime
    mdd : float
    rate_od_return : float
    sharpe_ratio : float
    total_asset : float
    total_principal : float
    total_profit : float
    volatility : float
    datestr : str
    timestr : str

def create_series(series, start, limit, rounding):
    series.index = series.index.strftime('%Y-%m-%d %H:%M:%S')
    series = series[series.index >= start]
    series = series.iloc[-limit:]
    series = series.apply(lambda x : round(x, rounding))
    return series
