#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jqdatasdk
from xqdata.api import history_bars

#input your jqdata username and password
jqdata_username = os.environ["JQDATA_USERNAME"]
jqdata_password = os.environ["JQDATA_PASSWORD"]
jqdatasdk.auth(username=jqdata_username, password=jqdata_password)

order_book_id = ['000001.XSHE',"300015.XSHE"]
end_date="2017-12-18"
frequency='1d'
bar_count = 10
skip_paused=False
fields = ['open', 'close', 'high', 'low', 'volume']
data = history_bars(order_book_ids=order_book_id, dt=end_date, frequency="1d", fields=fields, bar_count=bar_count, skip_suspended=skip_paused)