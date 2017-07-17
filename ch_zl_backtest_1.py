import pandas as pd
import numpy as np

from zipline.api import symbol, order, record, sid, get_datetime, order_target_percent, schedule_function, date_rules, time_rules
from zipline import run_algorithm
import pytz

class zl_backtest():
    def __init__(self, dict_dt_sec_wgt): #)
        self.dict_dt_sec_wgt = dict_dt_sec_wgt
        self.lst_assets = [str(x) for x in dict_dt_sec_wgt.values()[0].keys()] # 

    def initialize(self, context):
        """
        initialize() is called once at the start of the program. Any one-time
        startup logic goes here.
        """
        context.security_list = []
        for i in self.lst_assets:
            context.security_list.append(symbol(i))

    def compute_weights(self, context, data):
        """
        Compute weights for each security that we want to order.
        """
        c_date = get_datetime()#.date()

        lst_sorted_keys = self.dict_dt_sec_wgt.keys()
        lst_sorted_keys.sort()
        keys = []
        for i in lst_sorted_keys:
            if i < c_date:
                keys.append(i)
        c_date_idx = keys[-1]

        # log.info(normalized_weights)
        # log.info(context.security_list)
        weights = self.dict_dt_sec_wgt[c_date_idx] # {'F': 0.8, 'MSFT': -0.1}

        # Return our normalized weights. These will be used when placing orders later.
        return weights

    def rebalance(self, context, data):
        """
        This function is called according to our schedule_function settings and calls
        order_target_percent() on every security in weights.
        """

        weights = self.compute_weights(context, data)

        # Place orders for each of our securities.
        for security in context.security_list:
            if data.can_trade(security):
                order_target_percent(security, weights[security.symbol])

        # Check how many long and short positions we have.
        longs = shorts = 0
        for position in context.portfolio.positions.itervalues():
            if position.amount > 0:
                longs += 1
            elif position.amount < 0:
                shorts += 1

        # Record our variables.
        # record(ticker= context.security_list, leverage=context.account.leverage, long_count=longs, short_count=shorts)
        record(ticker=context.security_list[0], leverage=context.account.leverage, long_count=longs, short_count=shorts)



def get_perf(dict_dt_sec_wgt, initial_amount, start, end):
    stg_analyze = zl_backtest(dict_dt_sec_wgt)
    res = run_algorithm(start=start, end=end, initialize=stg_analyze.initialize, capital_base=initial_amount, handle_data=stg_analyze.rebalance, bundle='quantopian-quandl')
    res.to_pickle('res3.pkl')
    return res

if __name__ == '__main__':
    
    dict_dt_sec_wgt = {pd.datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc): {'F': 0.4, 'MSFT': -0.3}, 
                                        pd.datetime(2015, 2, 1, 0, 0, 0, 0, pytz.utc): {'F': 0.8, 'MSFT': -0.1}}

    start = pd.datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = pd.datetime(2016, 1, 1, 0, 0, 0, 0, pytz.utc)
    res = get_perf(dict_dt_sec_wgt, 1000000, start, end )
    
