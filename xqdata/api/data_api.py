import datetime
import pandas as pd

from xqdata.data_proxy import DataProxy


__all__ = []

def export_as_api(func):
    __all__.append(func.__name__)
    globals()[func.__name__] = func
    return func

@export_as_api
def history_bars(order_book_ids, bar_count, frequency, fields=None, dt=None, skip_suspended=False, include_now=True, adjust_type='pre',adjust_orig=None):
    """
    :param order_book_id: 合约代码
    :type order_book_id: `str`
    :param int bar_count: 获取的历史数据数量，必填项
    :param str frequency: 获取数据什么样的频率进行。'1d'或'1m'分别表示每日和每分钟，必填项
    :param str fields: 返回数据字段。必填项。见下方列表。
    =========================   ===================================================
    fields                      字段名
    =========================   ===================================================
    datetime                    时间戳
    open                        开盘价
    high                        最高价
    low                         最低价
    close                       收盘价
    volume                      成交量
    total_turnover              成交额
    open_interest               持仓量（期货专用）
    basis_spread                期现差（股指期货专用）
    settlement                  结算价（期货日线专用）
    prev_settlement             结算价（期货日线专用）
    =========================   ===================================================
    :param bool skip_suspended: 是否跳过停牌数据
    :param bool include_now: 是否包含当前数据
    :param str adjust_type: 复权类型，默认为前复权 pre；可选 pre, none, post
    :return: `ndarray`, 方便直接与talib等计算库对接，效率较history返回的DataFrame更高。
    """
    
    data_proxy = DataProxy.get_instance()
    if dt is None:
        dt = datetime.datetime.now()
    
    if frequency[-1] not in {'d',"w","M"}:
        raise TypeError("only support 'd','w' and 'M' frequency data type")
    if fields is None:
        fields = ["date", "open", "high", "low", "close", "volume"]

    bars =  data_proxy.history_bars(order_book_ids=order_book_ids, bar_count=bar_count, frequency=frequency, fields=fields, dt=dt,
                                    skip_suspended=skip_suspended, include_now=include_now,
                                    adjust_type=adjust_type, adjust_orig=adjust_orig)        
    return bars