#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jqdatasdk
import pandas as pd
from xqdata.base_data_source.default_data_source import DefaultDataSource
import unittest

#input your jqdata username and password
jqdata_username = os.environ["JQDATA_USERNAME"]
jqdata_password = os.environ["JQDATA_PASSWORD"]
jqdatasdk.auth(username=jqdata_username, password=jqdata_password)



#see https://github.com/JoinQuant/jqdatasdk/blob/master/tests/test_api.py
# ==================================================== #
# jqdata auth                                          #
# ==================================================== #


#
##from xqdata.data.base_data_source.history_fundamentals_jqdata import get_fundamentals_at_dt,get_fundamental_data, _history_bars_fundamentals_jq, history_bars_fundamentals_jq
##order_book_ids = ['000001.XSHE','600000.XSHG']
##fields = ["market_cap", "pe_ratio"]
##dt = "2019-08-20"
##dt_timestamp = pd.Timestamp(dt)
##
##data_at_dt = get_fundamentals_at_dt(order_book_ids=order_book_ids, fields=fields, dt=dt)
##data_bars = _history_bars_fundamentals_jq(order_book_ids=order_book_ids, fields=fields, bar_count=4,dt=dt)
##
##fields_with_turnover = ["market_cap", "pe_ratio","turnover_ratio"]
##data_daily= history_bars_fundamentals_jq(order_book_ids=order_book_ids, fields=fields_with_turnover, bar_count=4,dt=dt, frequency="1d")
##data_weekly= history_bars_fundamentals_jq(order_book_ids=order_book_ids, fields=fields_with_turnover, bar_count=4,dt=dt, frequency="1w")
##data_montly= history_bars_fundamentals_jq(order_book_ids=order_book_ids, fields=fields_with_turnover, bar_count=4,dt=dt, frequency="1M")
#
order_book_ids = ['000001.XSHE','600000.XSHG']
trading_fields = ["open","close"]
fundamental_fields = ["market_cap", "pe_ratio"]
all_fields = ["open","close", "market_cap", "pe_ratio"]
bar_count=4
dt = "2019-08-20"
frequency="1w"

data_source = DefaultDataSource() 
trading_data = data_source.history_tradings(order_book_ids=order_book_ids,bar_count=bar_count, frequency=frequency, dt=dt, fields=trading_fields)
fundamental_data = data_source.history_fundamentals(order_book_ids=order_book_ids,bar_count=bar_count, frequency=frequency, dt=dt, fields=fundamental_fields)
data = data_source.history_bars(order_book_ids=order_book_ids,bar_count=bar_count, frequency=frequency, dt=dt, fields=all_fields)
