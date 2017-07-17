import pandas as pd
import numpy as np

from zipline.api import symbol, order, record, sid, get_datetime, order_target_percent
from zipline import run_algorithm
import pytz

class stg():
    def __init__(self): #
    	pass

    def initial(self, context):
    	pass

    def handle_data(self, context, data):
    	order(symbol('AAPL'), 10)
    	record(AAPL=data.current(symbol('AAPL'), 'price'))

def get_perf(dict_dt_sec_wgt, initial_amount, start, end):
    stg_analyze = stg()

    res = run_algorithm(start=start, end=end, initialize=stg_analyze.initial,capital_base=initial_amount, handle_data=stg_analyze.handle_data, bundle='quantopian-quandl')
    res.to_pickle('res2.pkl')
    return res

if __name__ == '__main__':
    dict_dt_sec_wgt = {pd.datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc): {'AAPL': 0.4, 'MSFT': -0.3},
                       pd.datetime(2015, 2, 1, 0, 0, 0, 0, pytz.utc): {'AAPL': 0.8, 'MSFT': -0.1}}

    start = pd.datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = pd.datetime(2016, 1, 1, 0, 0, 0, 0, pytz.utc)
    get_perf(dict_dt_sec_wgt, 1000000, start, end )