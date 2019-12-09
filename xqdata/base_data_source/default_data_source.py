import pandas as pd
from xqdata.interface import AbstractDataSource
from jqdatasdk import get_bars, get_all_trade_days, get_index_stocks, get_industry
from xqdata.utils import convert_to_timestamp
from xqdata.base_data_source.indicator_mapping import ALL_INDICATOR_MAPPING

def parse_industry_code_dict(industry):
    data_container = {}
    for order_book_id, industry_dict in industry.items():
        industry_container = {}
        for criterion, industry_code_dict in industry_dict.items():
            industry_container[criterion] = industry_code_dict["industry_code"]
        data_container[order_book_id] = industry_container
    data_df = pd.DataFrame(data_container).transpose()
    data_df.index.name = "order_book_id"
    return data_df

class DefaultDataSource(AbstractDataSource):
    
    def history_tradings(self, order_book_ids, bar_count, frequency, dt, fields=['date','open','high','low','close'], skip_suspended=True, include_now=True, adjust_type="pre", adjust_orig=None):
        from xqdata.base_data_source.history_fundamentals_jqdata import history_tradings
        data = history_tradings(order_book_ids=order_book_ids, bar_count=bar_count, frequency=frequency, dt=dt, fields=fields, skip_suspended=skip_suspended, include_now=include_now, adjust_type=adjust_type, adjust_orig=adjust_orig)
        return data
        
    def history_fundamentals(self,order_book_ids, bar_count, frequency, dt, fields, skip_suspended=True, include_now=True, adjust_type="pre", adjust_orig=None):
        from xqdata.base_data_source.history_fundamentals_jqdata import history_bars_fundamentals_jq
        data_df = history_bars_fundamentals_jq(order_book_ids=order_book_ids, bar_count=bar_count, frequency=frequency, fields=fields, dt=dt)
        return data_df
    
    def history_bars(self, order_book_ids, bar_count, frequency, dt, fields, skip_suspended=True, include_now=True, adjust_type="pre", adjust_orig=None):
        
        trading_fields = []
        fundamental_fields = []
        for field in fields:
            if field in ['open', 'close', 'high', 'low', 'volume', 'money', 'factor', 'open_interest']:
                trading_fields.append(field)
            elif field in ALL_INDICATOR_MAPPING.keys():
                fundamental_fields.append(field)
            else:
                raise ValueError("{} is not support right now".format(field))

        if len(fundamental_fields) == 0:
            trading_data = self.history_tradings(order_book_ids=order_book_ids, bar_count=bar_count, frequency=frequency, dt=dt, fields=trading_fields, skip_suspended=skip_suspended, include_now=include_now, adjust_type=adjust_type, adjust_orig=adjust_orig)
            return trading_data
        elif len(trading_fields) == 0:
            fundamental_data = self.history_fundamentals(order_book_ids=order_book_ids, bar_count=bar_count, frequency=frequency, dt=dt, fields=fundamental_fields, skip_suspended=skip_suspended, include_now=include_now, adjust_type=adjust_type, adjust_orig=adjust_orig)
            return fundamental_data
        else:
            trading_data = self.history_tradings(order_book_ids=order_book_ids, bar_count=bar_count, frequency=frequency, dt=dt, fields=trading_fields, skip_suspended=skip_suspended, include_now=include_now, adjust_type=adjust_type, adjust_orig=adjust_orig)
            fundamental_data = self.history_fundamentals(order_book_ids=order_book_ids, bar_count=bar_count, frequency=frequency, dt=dt, fields=fundamental_fields, skip_suspended=skip_suspended, include_now=include_now, adjust_type=adjust_type, adjust_orig=adjust_orig)
            #pdb.set_trace()
            data = trading_data.merge(fundamental_data, left_index=True, right_index=True, how="outer")
            return data
    
    def get_trading_calendar(self):
        trading_dates = get_all_trade_days()
        #pdb.set_trace()
        trading_dates_timestamp = list(map(convert_to_timestamp, trading_dates))
        return pd.Index(trading_dates_timestamp)
    
    def index_components(self, order_book_id, dt=None):
        return get_index_stocks(index_symbol=order_book_id, date=dt)
    
    def get_instrument_industry(self, order_book_ids, dt=None):
        industry = get_industry(security=order_book_ids, date=dt)
        data_df = parse_industry_code_dict(industry)
        return data_df

    
