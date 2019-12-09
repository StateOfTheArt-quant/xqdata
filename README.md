# xqdata
**xqdata** is a high-level library to provide a clean and unified API for accessing financial data.
* xqdata provide a unified API to get trading data and fundamental data simultaneously
* xqdata provide a unified API for research and production environment
* xqdata is flexible and expandable, that means, you can change whatever the data source you want.

below is an example to show how to use xqdata
~~~
>>> from xqdata.api import history_bars
>>> data = history_bars(order_book_ids=["000001.XSHG", "000002.XSHG"], bar_count=4, frequency="1w", fields=["open","close", "market_cap", "pe_ratio"], dt="2019-08-20")
                           open  close  market_cap  pe_ratio
order_book_id datetime                                      
000001.XSHE   2019-08-02  14.25  13.74   2359.2146    9.1909
              2019-08-09  13.60  14.52   2493.1438    9.2858
              2019-08-16  14.61  14.90   2558.3914    9.5288
              2019-08-20  14.91  14.99   2573.8447    9.5864
600000.XSHG   2019-08-02  11.90  11.48   3369.6189    5.8029
              2019-08-09  11.42  11.37   3337.3315    5.7473
              2019-08-16  11.33  11.22   3293.3035    5.6715
              2019-08-20  11.22  11.37   3337.3315    5.7473
~~~

# Dependency
currently, xqdata is in alpha and now it is a high-level wrapper for open source financial data.
* [jqdatasdk](https://github.com/JoinQuant/jqdatasdk)

# Install
~~~
git clone https://github.com/StateOfTheArt-quant/xqdata.git
cd xqdata
python setup.py develop
~~~

# Quick start
~~~
import jqdatasdk
from xqdata.api import history_bars

#input your jqdata username and password
jqdatasdk.auth(username="188xxxxxxxx", password="xxxxxxxx")  #apply the username and code in https://www.joinquant.com/

order_book_ids = ['000001.XSHE','600000.XSHG']
all_fields = ["open","close", "market_cap", "pe_ratio"]
bar_count=4
dt = "2019-08-20"
frequency="1w"

data = history_bars(order_book_ids=order_book_ids, bar_count=bar_count, frequency=frequency, fields=all_fields, dt=dt)
~~~

# Documentation
[supported data fields](docs/supported_financial_fields.md)

# Author
Allen Yu (allen.across@gmail.com)

# License
This project following Apache 2.0 License as written in LICENSE file

Copyright 2018 Allen Yu, StateOfTheArt.quant, respective [rqalpha](https://github.com/ricequant/rqalpha) and [jqdata](https://github.com/JoinQuant/jqdatasdk) contributors


