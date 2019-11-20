import pandas as pd
from jqdatasdk import query, get_fundamentals, get_fundamentals_continuously, valuation, get_price, get_bars, get_all_trade_days
from xqdata.trading_dates_mixin import TradingDatesMixin
from xqdata.base_data_source.indicator_mapping import ALL_INDICATOR_MAPPING
from xqdata.utils import convert_to_timestamp

from xqdata.utils import convert_timestamp_to_str
import pdb

#def create_trading_dates_index():
#    trading_dates = get_all_trade_days()
#    pdb.set_trace()
#    trading_dates_timestamp = list(map(convert_to_timestamp, trading_dates))
#    return pd.Index(trading_dates_timestamp)
##
#trading_dates_index = create_trading_dates_index()
#trading_dates_mixin = TradingDatesMixin(trading_dates_index)

def history_tradings(order_book_ids, bar_count, frequency, dt, fields=['date','open','high','low','close'], skip_suspended=True, include_now=True, adjust_type="pre", adjust_orig=None):
    from xqdata.data_proxy import DataProxy
    #get_bars(security, count, unit='1d', fields=['date','open','high','low','close'], include_now=False, end_dt=None, fq_ref_date=None)
    if "date" not in fields:
        fields.append("date")
        
    dt = DataProxy.get_instance().get_next_trading_date(dt,n=1)
    data = get_bars(security=order_book_ids, count=bar_count, unit=frequency, end_dt=dt,fields=fields, include_now=include_now,fq_ref_date=adjust_orig)
    data["datetime"] = data["date"].apply(convert_to_timestamp)
    data = data.reset_index().rename(columns={"level_0":"order_book_id"})
    data = data.set_index(["order_book_id","datetime"])
    data = data.drop(columns=["level_1","date"])
    return data


def create_a_query_object(order_book_ids, fields):
    indicator_expr_list = []
    for indicator_str in fields:
        try:
            indicator_expr = ALL_INDICATOR_MAPPING[indicator_str]
        except KeyError:
            raise Exception("the indicator str:{} is not available".format(indicator_str))
        else:
            indicator_expr_list.append(indicator_expr)
    # support 1 and mant order_book_ids
    if isinstance(order_book_ids, str):
        query_object = query(valuation.code,*indicator_expr_list).filter(valuation.code.in_([order_book_ids]))
    elif isinstance(order_book_ids, list):
        query_object = query(valuation.code,*indicator_expr_list).filter(valuation.code.in_(order_book_ids))
    else:
        raise(Exception("order_book_id must be string or a list"))
    return query_object
    

def get_fundamentals_at_dt(order_book_ids, fields, dt):
    query_object = create_a_query_object(order_book_ids=order_book_ids, fields=fields)
    data_df = get_fundamentals(query_object, date=dt)
    # create multiindex
    data_df.set_index(['code'], inplace=True)
    data_df.rename_axis(index={"code": "order_book_id"}, inplace=True)
    return data_df

def get_fundamental_data(order_book_ids, fields, dt_list):
    data_container = {}
    for date in dt_list:
        data_df = get_fundamentals_at_dt(order_book_ids=order_book_ids, fields=fields, dt=date)
        dt = convert_to_timestamp(date)
        data_container[dt] = data_df
    data = pd.concat(data_container)
    data = data.swaplevel()
    data.index.names = ["order_book_id",'datetime']
    data.sort_index(level="order_book_id", inplace=True)
    return data
#
#
def _history_bars_fundamentals_jq(order_book_ids, bar_count, fields=None, dt=None):
    from xqdata.data_proxy import DataProxy
    # 
    start_date = DataProxy.get_instance().get_previous_trading_date(dt, n=bar_count)
    start_date = convert_timestamp_to_str(start_date)
    trading_dates = DataProxy.get_instance().get_trading_dates(start_date=start_date, end_date=dt)
    
    date_str_list = [convert_timestamp_to_str(timestamp) for timestamp in trading_dates]
    data_df = get_fundamental_data(order_book_ids=order_book_ids, fields=fields, dt_list=date_str_list)
    return data_df
#
def _merge_asof(data1, data2):
    data = pd.merge_asof(data1, data2, left_index=True, right_index=True, direction='backward') # to avoid future functionality
    return data
#
#
def history_bars_fundamentals_jq(order_book_ids, bar_count, frequency, fields=None, dt=None):
    from xqdata.data_proxy import DataProxy
    """
    return: [pd.Panel] 
           Items: date
           Major: order_boook_id
           Minor: fields
    """
    if (frequency[-1] not in ['d']) and (frequency not in ['1w', '1M']):
        raise Exception("only support xd, 1w and 1M data")
    
    if frequency == '1d':
        data_df = _history_bars_fundamentals_jq(order_book_ids=order_book_ids, bar_count=bar_count,fields=fields, dt=dt)
        return data_df
    
    dt = DataProxy.get_instance().get_next_trading_date(dt,n=1)
    trading_data = get_bars(security='000001.XSHG', count=bar_count, unit=frequency, fields=['date'], include_now=True, end_dt=dt, fq_ref_date=None)
    date_list = trading_data['date'].tolist()
    date_str_list = [date.strftime("%Y-%m-%d") for date in date_list]
    #pdb.set_trace() 
    if 'turnover_ratio' not in fields:
        data_df = get_fundamental_data(order_book_ids=order_book_ids, fields=fields, dt_list=date_str_list)
        return data_df
    else:
        fields.remove('turnover_ratio')
        data_df = get_fundamental_data(order_book_ids=order_book_ids, fields=fields, dt_list=date_str_list) # difference frequency
        # scale
        scale = 1
        if frequency[-1] == 'd':
            scale *= int(frequency[:-1])
        elif frequency == "1w":
            scale *= 5
        elif frequency == '1M':
            scale *= 20
        bar_count_ = bar_count * scale
        
        # get turnover_ratio data
        turnover_df = _history_bars_fundamentals_jq(order_book_ids=order_book_ids, bar_count=bar_count_, fields=['turnover_ratio'], dt=dt)['turnover_ratio']
        
        timestamp_list = [convert_to_timestamp(date_str) for date_str in date_str_list]
        frequency_date_df = pd.DataFrame(timestamp_list, index=timestamp_list, columns=['datetime'])
        frequency_date_df.index.name = "datetime"
        #pdb.set_trace()
        turnover = frequency_date_df.join(turnover_df,how='outer')
        
        turnover['datetime1'] = turnover.groupby(level="order_book_id")['datetime'].fillna(method="bfill")
        turnover = turnover.reset_index(level="order_book_id").groupby(by=['order_book_id','datetime1'])["turnover_ratio"].sum()
        turnover.rename_axis(index={"datetime1": "datetime"}, inplace=True)
        
        data = turnover.to_frame().join(data_df, how='outer')
        return data  
