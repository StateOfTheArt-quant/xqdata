class AbstractDataSource(object):
    """
    Data source interface. if you want to realize backtest, paper trading or living trading,
    you need to create a data souce which inherit this abstract interface, and then realize the methods below
    """
    # ----basic trading data and fundamental data-------------------------------------------------
    def history_bars(self, order_book_id, bar_count, frequency, dt, fields, skip_suspended=True, include_now=False, adjust_type="pre", adjust_orig=None):
        raise NotImplementedError
        
    def history_tradings(self, order_book_ids, bar_count, frequency, dt, fields, skip_suspended=True, include_now=False, adjust_type="pre", adjust_orig=None):
        raise NotImplementedError
    
    def history_fundamentals(self, order_book_ids, bar_count, frequency, dt, fields, skip_suspended=True, include_now=False, adjust_type="pre", adjust_orig=None):
        raise NotImplementedError
                
    def get_trading_calendar(self):
        raise NotImplementedError
    
    def index_components(self, order_book_id, dt):
        raise NotImplementedError
    
    def get_instrument_industry(self, order_book_id, dt):
        raise NotImplementedError
        
        