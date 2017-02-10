
from pybtcc.api import btcc, btccAPIRateLimitError
from . import utils

import os
import pandas as pd
import time
import logging

logger = logging.getLogger(__name__)

# Set pybtcc to warning only
logging.getLogger("pybtcc").setLevel(logging.DEBUG)

"""
Notes:
    - Everything is in seconds since EPOCH unless the api or something needs it
    converted
"""


class Collector(utils.BaseCollector):
    """TODO """
    def __init__(self, dataFile=None, dataDir=None, api=None):
        super(Collector, self).__init__(dataDir)
        self.logger = logging.getLogger(__name__)
        if dataFile is not None:
            self.dataFile = dataFile
        else:
            self.dataFile = 'btcc_' + self.dataFile
        self.dataPath = os.path.join(self.dataDir, self.dataFile)
        if api is None:
            self.api = btcc('', '')
            self.logger.warning('API not provided and no auth found.' +
                                'Using non-authenticated (Reduced Rates)')
        else:
            self.api = api
        self._stop_time()

    def new_collection(self, fromtime):
        self._check_new_collection()
        df = self._get_data(fromtime, new=True)
        self._save_dataframe(df)
        self.logger.info('Complete. New collection fetched.')

    def collect(self):
        with pd.HDFStore(os.path.join(self.dataDir, self.dataFile)) as store:
            nrows = store.get_storer('trades').nrows
            lastval = store.select('trades', start=nrows - 1, stop=nrows)
            fromtime = ((lastval.index.astype(int).max())/10e8)
            fromid = lastval.tid
            self.logger.info('Last fetched time is: {}'.format(
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(fromtime))))
        df = self._get_data(fromid)
        self._save_dataframe(df)
        self.logger.info('Complete. {} new trades added.'.format(len(df)))

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
                self.logger.error(e)
            if dft.empty:
                break
            fetchedid = dft.tid[-1]
            fetchedtime = ((dft.index.astype(int).max())/10e8)
            df = pd.concat([df, dft])
            df = self._partial_save(df)
            self.logger.info('Getting data... Last call got to: {}'.format(
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(fetchedtime))))
        return df

    def _last_fetched(self):
        pass

    def _data_check(self):
        if os.path.isfile(os.path.join(self.dataDir, self.dataFile)):
            return 2
        elif os.path.isdir(self.dataDir):
            return 1
        else:
            return 0


class btccSaver(utils.BaseClass):
    """TODO """
    def __init__(self):
        super(btccSaver, self).__init__()
