# 证券代码标准格式

由于同一代码可能代表不同的交易品种，xqdata沿用量化主流的代码后缀，用户在调用API时，需要将参数order_book_id传入带有该市场后缀的证券代码，如order_book_ids=['600519.XSHG']，以便于区分实际调用的交易品种。以下列出了每个交易市场的代码后缀和示例代码。
~~~
交易市场	代码后缀	示例代码	证券简称
上海证券交易所	.XSHG	'600519.XSHG'	贵州茅台
深圳证券交易所	.XSHE	'000001.XSHE'	平安银行
中金所	.CCFX	'IC9999.CCFX'	中证500主力合约
大商所	.XDCE	'A9999.XDCE'	豆一主力合约
上期所	.XSGE	'AU9999.XSGE'	黄金主力合约
郑商所	.XZCE	'CY8888.XZCE'	棉纱期货指数
上海国际能源期货交易所	.XINE	'SC9999.XINE'	原油主力合约
~~~

# 2 支持的数据字段

## 2.1 支持的交易数据字段
~~~
open: 开盘价
high: 最高价
low: 最低价，
close: 收盘价
volume: 成交量
money: 成交额
~~~

## 2.2 支持的财务数据字段
[财务数据字段](https://www.joinquant.com/help/api/help?name=Stock#财务数据列表)