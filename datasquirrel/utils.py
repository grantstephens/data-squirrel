import logging
import os.path
import time
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LIB_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
AUTH_FILE = 'auth.json'
DATA_FILE = 'data.h5'

logger = logging.getLogger(__name__)
# logging.getLogger("pyluno").setLevel(logging.WARNING)


class BaseClass(object):
    """docstring for """
    def __init__(self):
        self.rootDir = ROOT_DIR
        self.dataDir = DATA_DIR
        self.dataFile = DATA_FILE
        self.authFile = AUTH_FILE


class BaseCollector(BaseClass):
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
            self.logger.info(
                'Path did not exist. Created: {}'.format(self.dataDir)
                )

    def _stop_time(self):
        self.stoptime = time.time()

    def _save_dataframe(self, df):
        with pd.HDFStore(self.dataPath, format='table',
                         complevel=9, complib='blosc') as store:
            store.append('trades', df, format='table')

    def _partial_save(self, df):
        if len(df) >= 10000:
            self.logger.info(
                'Large dataframe. Writing to {} trades to disc'.format(len(df))
                )
            self._save_dataframe(df)
            df = pd.DataFrame()
        return df
