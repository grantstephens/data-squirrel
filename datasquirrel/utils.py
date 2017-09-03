import json
import logging
import os.path
import time

import pandas as pd
import pkg_resources

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LIB_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
AUTH_FILE = 'auth.json'
DATA_FILE = 'data.h5'

log = logging.getLogger(__name__)


class BaseClass(object):
    """docstring for """

    def __init__(self):
        # self.log = logging.getLogger(__class__)
        self.root_dir = ROOT_DIR
        self.data_dir = DATA_DIR
        self.data_file = DATA_FILE
        self.auth_file = AUTH_FILE


class BaseCollector(BaseClass):
    """TODO"""
    def __init__(self, child, data_dir=None, data_file=None, auth_file=None):
        super(BaseCollector, self).__init__()
        # import ipdb; ipdb.set_trace()
        self.log = logging.getLogger(self.__class__.__name__)
        if data_dir is not None:
            self.data_dir = data_dir
        if data_file is not None:
            self.data_file = data_file
        else:
            self.data_file = child+'_' + self.data_file
        self.data_dir = os.path.join(self.data_dir, self.data_file)
        if auth_file is not None:
            self.auth_file = auth_file
        self._load_auth(child)

    def _check_new_collection(self):
        if os.path.isfile(self.data_dir):
            raise Exception('File Exists! Delete {} before starting a new\
                            collection'.format(self.data_dir))
        if not os.path.exists(os.path.dirname(self.data_dir)):
            os.makedirs(os.path.dirname(self.data_dir))
            self.log.info(
                'Path did not exist. Created: {}'.format(
                    os.path.dirname(self.data_dir))
                )

    def _stop_time(self):
        if not hasattr(self, 'stoptime'):
            self.stoptime = time.time()
        if time.time() > self.stoptime + 120:
            self.stoptime = time.time()
            self.log.info('Updated stop time to current time')

    def _save_dataframe(self, df):
        with pd.HDFStore(self.data_dir, format='table',
                         complevel=9, complib='blosc') as store:
            store.append('trades', df, format='table')

    def _partial_save(self, df):
        if len(df) >= 10000:
            self.log.info(
                'Large dataframe. Writing to {} trades to disc'.format(len(df))
                )
            self._save_dataframe(df)
            df = pd.DataFrame()
        self._stop_time()  # Update stop time if needed
        return df

    def _load_auth(self, child):
        self.auth = {}
        if os.path.isfile(os.path.join(self.root_dir, self.auth_file)):
            with open(os.path.join(self.root_dir, self.auth_file)) \
             as auth_file:
                auth = json.load(auth_file)
        elif os.path.isfile(self.auth_file):
            with open(self.auth_file) as auth_file:
                auth = json.load(auth_file)
        if child+'_key' in auth.keys():
            self.auth = auth
            self.log.info('Create authenticated API')
        else:
            self.auth[child+'_key'] = None
            self.auth[child+'_secret'] = None
            self.log.warning('API not provided and no auth found.' +
                             'Using non-authenticated (Reduced Rates)')
