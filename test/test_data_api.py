#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
import jqdatasdk
from xqdata.api import history_bars, index_components, get_instrument_industry

#input your jqdata username and password
jqdata_username = os.environ["JQDATA_USERNAME"]
jqdata_password = os.environ["JQDATA_PASSWORD"]
jqdatasdk.auth(username=jqdata_username, password=jqdata_password)


order_book_ids = ['000001.XSHE','600000.XSHG']
trading_fields = ["open","close"]
fundamental_fields = ["market_cap", "pe_ratio"]
all_fields = ["open","close", "market_cap", "pe_ratio"]
bar_count=4
dt = "2019-08-20"
frequency="1w"

data = history_bars(order_book_ids=order_book_ids, bar_count=bar_count, frequency=frequency, fields=all_fields, dt=dt)
index_components_list = index_components(order_book_id="000300.XSHG")
industry_df = get_instrument_industry(order_book_ids=order_book_ids)