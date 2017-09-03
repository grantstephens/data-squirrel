
import json
import logging
import os
import time

import pandas as pd

from pyluno.api import Luno, LunoAPIRateLimitError

from .utils import BaseCollector

logger = logging.getLogger(__name__)

# Set pyluno to warning only
logging.getLogger("pyluno").setLevel(logging.WARNING)

"""
Notes:
    - Everything is in seconds since EPOCH unless the api or something needs it
    converted
"""


class LunoCollector(BaseCollector):
    """Luno Collector."""

    def __init__(self, data_dir=None, data_file=None, auth_file=None, api=None):
        super(LunoCollector, self).__init__('luno', data_dir, data_file, auth_file)
        if api is None:
            options = {'maxRate': 0.1, 'maxBurst': 5}
            self.api = Luno(self.auth['luno_key'], self.auth['luno_secret'],
                            options)
        else:
            self.api = api
        self._stop_time()

    def new_collection(self, fromtime):
        self._check_new_collection()
        df = self._get_data(fromtime)
        self._save_dataframe(df)
        self.log.info('Complete. New collection fetched.')

    def collect(self):
        self._check_existing_collection()
        with pd.HDFStore(self.data_dir) as store:
            nrows = store.get_storer('trades').nrows
            lastval = store.select('trades', start=nrows - 1, stop=nrows)
            fromtime = ((lastval.index.astype(int).max())/10e8)
            self.log.info('Last fetched time is: {}'.format(
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(fromtime))))
        df = self._get_data(fromtime)

        self._save_dataframe(df)
        self.log.info('Complete. {} new trades added.'.format(len(df)))

    def _get_data(self, fromtime, df=pd.DataFrame()):
        fetchedtime = fromtime
        while fetchedtime < int(self.stoptime):
            try:
                dft = self.api.market.get_trades_frame(
                    since=int(round(fetchedtime*1000)))
            except LunoAPIRateLimitError as e:
                dft = pd.DataFrame()
                self.log.error(e)
            if dft.empty:
                break
            fetchedtime = ((dft.index.astype(int).max())/10e8)
            df = pd.concat([df, dft])
            df = self._partial_save(df)
            self.log.info('Getting data... Last call got to: {}'.format(
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(fetchedtime))))
        return df
