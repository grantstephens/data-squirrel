
import json
import logging
import os
import time

import pandas as pd

from pygooglefinance.api import GoogleFinance, GoogleFinanceAPIRateLimitError

from . import utils

# logger = logging.getLogger(__name__)

# Set pygooglefinance to warning only
logging.getLogger("pygooglefinance").setLevel(logging.WARNING)

"""
Notes:
    - Everything is in seconds since EPOCH unless the api or something needs it
    converted
"""


class GFCollector(utils.BaseCollector):
    """TODO """
    def __init__(self, ticker, data_dir=None, data_file=None, api=None):
        super(GFCollector, self).__init__(ticker.lower(), data_dir, data_file)
        # self.log = logging.getLogger(__name__)
        self.ticker = ticker
        if api is None:
            self.api = GoogleFinance(self.ticker)
        else:
            self.api = api
        self._stop_time()

    def new_collection(self):
        self._check_new_collection()
        period = '20Y'  # Max
        df = self._get_data(86400, period)
        for interval in [3600, 1800, 900, 600, 300, 120, 60]:
            dft = self._get_data(interval, period)
            df = pd.concat([df[:dft.index[0]], dft])
        self._save_dataframe(df)
        self.log.info('Complete. New collection fetched.')

    def collect(self):
        with pd.HDFStore(self.data_dir) as store:
            nrows = store.get_storer('trades').nrows
            lastval = store.select('trades', start=nrows - 1, stop=nrows)
            fromtime = ((lastval.index.astype(int).max())/10e8)
            self.log.info('Last fetched time is: {}'.format(
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(fromtime))))

        df = self._get_data(60, '1M')
        df = df[pd.to_datetime(fromtime, unit='s'):].iloc[1:]
        self._save_dataframe(df)
        self.log.info('Complete. {} new trades added.'.format(len(df)))

    def _get_data(self, interval, period):
        try:
            df = self.api.get_prices_frame(self.ticker,
                                           interval, period)
            df.drop(['high', 'low', 'open', 'volume'], axis=1, inplace=True)
        except GoogleFinanceAPIRateLimitError as e:
            df = pd.DataFrame()
            self.log.error(e)
        stime = ((df.index.astype(int).min())/10e8)
        # df = self._partial_save(df)
        self.log.info('Getting data... Last call started at: {}'.format(
            time.strftime('%Y-%m-%d %H:%M:%S',
                          time.localtime(stime))))
        return df
