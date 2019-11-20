import pandas as pd
import datetime

def convert_to_timestamp(date):
    if isinstance(date, pd.Timestamp):
        return date
    elif isinstance(date,(str, datetime.date, datetime.datetime)):
        return pd.Timestamp(date)
    else:
        raise Exception("date should be pandas.Timestamp, str date, datetime.date")

def convert_str_to_timestamp(str_dt):
    return pd.Timestamp(str_dt)

def convert_timestamp_to_str(timestamp, format='%Y-%m-%d'):
    return convert_timestamp_to_dt(timestamp).strftime(format)

def convert_timestamp_to_dt(timestamp):
    return timestamp.to_pydatetime()


def convert_str_to_dt(str_dt, format_="%Y-%m-%d %H:%M:%S"):
    """convert str tpye to datetime"""
    # "%Y-%m-%d %H:%M:%S.%f"
    # "%m/%d/%Y %H:%M:%S.%f"
    dt = datetime.datetime.strptime(str_dt, format_)
    return dt
