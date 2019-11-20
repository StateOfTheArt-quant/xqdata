import pandas as pd
from xqdata.interface import AbstractDataSource
from jqdatasdk import get_bars, get_all_trade_days
from xqdata.utils import convert_to_timestamp
from xqdata.base_data_source.indicator_mapping import ALL_INDICATOR_MAPPING


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

    
