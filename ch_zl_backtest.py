import pandas as pd
import numpy as np

from zipline.api import symbol, order, record, sid, get_datetime, order_target_percent, schedule_function, date_rules, time_rules
from zipline import run_algorithm
import pytz

class zl_backtest():
    def __init__(self, , dict_dt_sec_wgt): #)
        self.dict_dt_sec_wgt = dict_dt_sec_wgt
        self.lst_assets = [str(x) for x in dict_dt_sec_wgt.values()[0].keys()] # 

    def initialize(self, context):
        """
        initialize() is called once at the start of the program. Any one-time
        startup logic goes here.
        """

        # An assortment of securities from different sectors:
        # MSFT, UNH, CTAS, JNS, COG    sid(5061), 
        context.security_list = [symbol("MSFT"), symbol('UNH'), symbol('CTAS'), symbol('JNS'), symbol('COG')]
        #context.security_list = [sid(5061), sid(7792), sid(1941), sid(24556), sid(1746)]

        # Rebalance every Monday (or the first trading day if it's a holiday)
        # at market open.
        schedule_function(self.rebalance,
                          date_rules.week_start(days_offset=0),
                          time_rules.market_open())

        # Record variables at the end of each day.
        schedule_function(self.record_vars,
                          date_rules.every_day(),
                          time_rules.market_close())

    def compute_weights(self, context, data):
        """
        Compute weights for each security that we want to order.
        """
        # Get the 30-day price history for each security in our list.
        hist = data.history(context.security_list, 'price', 30, '1d')

        # Create 10-day and 30-day trailing windows.
        prices_10 = hist[-10:]
        prices_30 = hist

        # 10-day and 30-day simple moving average (SMA)
        sma_10 = prices_10.mean()
        sma_30 = prices_30.mean()


        # Weights are based on the relative difference between the short and long SMAs
        raw_weights = (sma_30 - sma_10) / sma_30
        # Normalize our weights
        normalized_weights = raw_weights / raw_weights.abs().sum()

        # Determine and log our long and short positions.
        short_secs = normalized_weights.index[normalized_weights < 0]
        long_secs = normalized_weights.index[normalized_weights > 0]


        # Return our normalized weights. These will be used when placing orders later.
        return normalized_weights

    def rebalance(self, context, data):
        """
        This function is called according to our schedule_function settings and calls
        order_target_percent() on every security in weights.
        """

        # Calculate our target weights.
        weights = self.compute_weights(context, data)

        # Place orders for each of our securities.
        for security in context.security_list:
            if data.can_trade(security):
                order_target_percent(security, weights[security])

    def record_vars(self, context, data):
        """
        This function is called at the end of each day and plots our leverage as well
        as the number of long and short positions we are holding.
        """

        # Check how many long and short positions we have.
        longs = shorts = 0
        for position in context.portfolio.positions.itervalues():
            if position.amount > 0:
                longs += 1
            elif position.amount < 0:
                shorts += 1

        # Record our variables.
        record(leverage=context.account.leverage, long_count=longs, short_count=shorts)


def get_perf(dict_dt_sec_wgt, initial_amount, start, end):
    stg_analyze = zl_backtest()
    res = run_algorithm(start=start, end=end, initialize=stg_analyze.initialize, capital_base=initial_amount, handle_data=stg_analyze.rebalance, bundle='quantopian-quandl')
    res.to_pickle('res2.pkl')
    return res

if __name__ == '__main__':
    
    dict_dt_sec_wgt = {pd.datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc): {'AAPL': 0.4, 'MSFT': -0.3}, 
                                        pd.datetime(2015, 2, 1, 0, 0, 0, 0, pytz.utc): {'AAPL': 0.8, 'MSFT': -0.1}}

    start = pd.datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = pd.datetime(2016, 1, 1, 0, 0, 0, 0, pytz.utc)
    res = get_perf(dict_dt_sec_wgt, 1000000, start, end )
    
