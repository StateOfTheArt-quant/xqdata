#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xqdata.data_proxy import DataProxy

__all__ = []

def export_as_api(func):
    __all__.append(func.__name__)
    globals()[func.__name__] = func
    return func

@export_as_api
def index_components(order_book_id, dt=None):
    return DataProxy.get_instance().index_components(order_book_id=order_book_id, dt=dt)

@export_as_api
def get_instrument_industry(order_book_ids, dt=None):
    return DataProxy.get_instance().get_instrument_industry(order_book_ids=order_book_ids, dt=dt)
