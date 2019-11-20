from xqdata.data_proxy import DataProxy

__all__ = []

def export_as_api(func):
    __all__.append(func.__name__)
    globals()[func.__name__] = func
    return func

@export_as_api
def get_trading_dates(start_date, end_date):
    """
    获取某个国家市场的交易日列表（起止日期加入判断）。目前仅支持中国市场。
    :param start_date: 开始日期
    :type start_date: `str` | `date` | `datetime` | `pandas.Timestamp`
    :param end_date: 结束如期
    :type end_date: `str` | `date` | `datetime` | `pandas.Timestamp`
    :return: list[`datetime.date`]
    :example:
    ..  code-block:: python3
        :linenos:
        [In]get_trading_dates(start_date='2016-05-05', end_date='20160505')
        [Out]
        [datetime.date(2016, 5, 5)]
    """
    return DataProxy.get_instance().get_trading_dates(start_date, end_date)

@export_as_api
def get_previous_trading_date(date, n=1):
    return DataProxy.get_instance().get_previous_trading_date(date, n)

@export_as_api
def get_next_trading_date(date, n=1):
    return DataProxy.get_instance().get_next_trading_date(date, n)

@export_as_api
def get_trading_calendar():
    """
    获取中国A股当年所有的交易日期列表
    return pd.Series
    """
    return DataProxy.get_instance().get_trading_calendar()

