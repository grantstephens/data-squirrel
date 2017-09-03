
import logging
import os
import time

import pandas as pd

from pybtcc.api import btcc, btccAPIRateLimitError

from .utils import BaseCollector

logger = logging.getLogger(__name__)

# Set pybtcc to warning only
logging.getLogger("pybtcc").setLevel(logging.DEBUG)

"""
Notes:
    - Everything is in seconds since EPOCH unless the api or something needs it
    converted
"""


class BTCCCollector(BaseCollector):
    """BTCC Collector."""

    def __init__(self, data_dir=None, data_file=None, auth_file=None, api=None):
        super(BTCCCollector, self).__init__('btcc', data_dir, data_file, auth_file)
        if api is None:
            options = {'maxRate': 10, 'maxBurst': 50}
            self.api = btcc(self.auth['btcc_key'], self.auth['btcc_secret'],
                            options)
        else:
            self.api = api
        self._stop_time()

    def new_collection(self, fromtime):
        self._check_new_collection()
        df = self._get_data(fromtime, new=True)
        self._save_dataframe(df)
        self.log.info('Complete. New collection fetched.')

    def collect(self):
        with pd.HDFStore(self.data_dir) as store:
            nrows = store.get_storer('trades').nrows
            lastval = store.select('trades', start=nrows - 1, stop=nrows)
            fromtime = ((lastval.index.astype(int).max())/10e8)
            fromid = lastval.tid
            self.log.info('Last fetched time is: {}'.format(
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(fromtime))))
        df = self._get_data(fromid)
        self._save_dataframe(df)
        self.log.info('Complete. {} new trades added.'.format(len(df)))

    def _get_data(self, fromid, df=pd.DataFrame(), new=False):
        if new:
            dft = self.api.get_trades_frame(
                limit=5000, since=int(round(fromid)), sincetype='time')
            fetchedid = dft.tid[-1]
            fetchedtime = ((dft.index.astype(int).max())/10e8)
            # print(dft)
        else:
            fetchedid = fromid
            fetchedtime = 0  # To get into while
        while fetchedtime < int(self.stoptime):
            try:
                dft = self.api.get_trades_frame(
                    limit=5000, since=fetchedid, sincetype='id')
            except btccAPIRateLimitError as e:
                dft = pd.DataFrame()
                self.log.error(e)
            if dft.empty:
                break
            fetchedid = dft.tid[-1]
            fetchedtime = ((dft.index.astype(int).max())/10e8)
            df = pd.concat([df, dft])
            df = self._partial_save(df)
            self.log.info('Getting data... Last call got to: {}'.format(
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(fetchedtime))))
        return df
