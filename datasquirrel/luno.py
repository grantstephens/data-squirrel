
from pyluno.api import Luno
from . import utils

import os
import math
# import numpy as np
import pandas as pd
import time
import logging

logger = logging.getLogger(__name__)

# Set pyluno to warning only
logging.getLogger("pyluno").setLevel(logging.WARNING)

"""
Notes:
    - Everything is in seconds since EPOCH unless the api or something needs it
    converted
"""


class BaseCollector(utils.BaseClass):
    """TODO"""
    def __init__(self, dataDir=None):
        super(BaseCollector, self).__init__()
        if dataDir is not None:
            self.dataDir = dataDir

    def _check_new_collection(self):
        if os.path.isfile(self.dataPath):
            raise Exception('File Exists! Delete {} before starting a new\
                            collection'.format(self.dataPath))
        if not os.path.exists(self.dataDir):
            os.makedirs(self.dataDir)
            logger.info('Path did not exist. Created: {}'.format(self.dataDir))

    def _stop_time(self):
        self.stoptime = time.time()


class LunoCollector(BaseCollector):
    """TODO """
    def __init__(self, dataFile=None, dataDir=None, api=None):
        super(LunoCollector, self).__init__(dataDir)
        if dataFile is not None:
            self.dataFile = dataFile
        else:
            self.dataFile = 'luno_' + self.dataFile
        self.dataPath = os.path.join(self.dataDir, self.dataFile)
        if api is None:
            self.api = Luno('', '')
            logger.warning('API not provided. Created one with no authentication')
        self._stop_time()

    def new_collection(self, fromdate):
        # self._check_new_collection()
        fetchedtime = fromdate
        df = pd.DataFrame()
        while fetchedtime < int(self.stoptime):
            dft = self.api.get_trades_frame(since=int(round(fetchedtime*1000)))
            if dft.empty:
                break
            fetchedtime = ((dft.index.astype(int).max())/10e8)
            df = pd.concat([df, dft])
            if len(df) > 1000000:
                pass
                logger.warning('Large df')
                # TODO: Write dataframe to file, clear dataframe end carry on
            logger.info('Getting data... Last call got to: {}'.format(
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(fetchedtime))))
        with pd.HDFStore(self.dataPath, format='table') as store:
            store.append('trades', df, complevel=5, format='table')
        logger.info('Complete. New collection fetched.')

    def collect(self):
        pass

    def _last_fetched(self):
        pass

    def _data_check(self):
        if os.path.isfile(os.path.join(self.dataDir, self.dataFile)):
            return 2
        elif os.path.isdir(self.dataDir):
            return 1
        else:
            return 0


class LunoSaver(utils.BaseClass):
    """TODO """
    def __init__(self):
        super(LunoSaver, self).__init__()
