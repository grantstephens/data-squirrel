"""Utilities used by the squirrel."""
import json
import logging
import os.path
import threading
import time

import pandas as pd
import pkg_resources

ROOT_DIR = os.path.join(
    os.path.dirname(
        pkg_resources.resource_filename(__name__, 'utils.py'))
    , '..')
LIB_DIR = os.path.join(ROOT_DIR, 'datasquirrel')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
AUTH_FILE = 'auth.json'
DATA_FILE = 'data.h5'


class BaseClass(object):
    """Class with common variables."""

    def __init__(self, data_dir):
        """Make new with the given data directory."""
        self.log = logging.getLogger(self.__class__.__name__)
        self.root_dir = ROOT_DIR
        self.data_file = DATA_FILE
        self.auth_file = AUTH_FILE
        if data_dir is not None:
            self.data_dir = data_dir
            if os.path.exists(os.path.join(
                    os.path.dirname(data_dir), 'auth.json')):
                self.auth_file = os.path.join(
                    os.path.dirname(data_dir), 'auth.json')
                self.log.info('Found auth.json in data directory.' +
                              ' Will use it unless other auth file was given.')
        else:
            self.data_dir = DATA_DIR


class BaseCollector(BaseClass):
    """Base Collector class with common methods."""

    def __init__(self, child, data_dir=None, data_file=None, auth_file=None):
        """Made new base collector using some child data."""
        super(BaseCollector, self).__init__(data_dir)
        self.log = logging.getLogger(
        self.__class__.__name__+' ({})'.format(child))

        if data_file is not None:
            self.data_file = data_file
        else:
            self.data_file = child+'_' + self.data_file
        self.data_dir = os.path.join(self.data_dir, self.data_file)
        if auth_file is not None:
            self.auth_file = auth_file
            self.log.info('Using given auth file')
        else:
            if not os.path.exists(self.auth_file):
                self.log.warning(
                    'auth.json not found. Using example_auth.json')
                self.auth_file = os.path.join(
                    os.path.dirname(self.auth_file), 'example_auth.json')
        self._load_auth(child)

    def _check_new_collection(self):
        if os.path.isfile(self.data_dir):
            msg = 'File Exists! Delete {} before starting a new\
                collection'.format(self.data_dir)
            self.log.exception(msg)
            raise Exception(msg)
        if not os.path.exists(os.path.dirname(self.data_dir)):
            os.makedirs(os.path.dirname(self.data_dir), exist_ok=True)
            self.log.info(
                'Path did not exist. Created: {}'.format(
                    os.path.dirname(self.data_dir))
                )

    def _check_existing_collection(self):
        if not os.path.isfile(self.data_dir):
            msg = 'Data file does not exist: {}'.format(self.data_dir)
            self.log.exception(msg)
            raise Exception(msg)

    def _stop_time(self):
        if not hasattr(self, 'stoptime'):
            self.stoptime = time.time()
        if time.time() > self.stoptime + 120:
            self.stoptime = time.time()
            self.log.info('Updated stop time to current time')

    def _save_dataframe(self, df):
        with pd.HDFStore(self.data_dir, format='table',
                         complevel=9, complib='zlib') as store:
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
                             'Using non-authenticated (Reduced rates)')


class NutRoute (threading.Thread):
    """Threading the different nuts."""

    def __init__(self, nut, action='forrage', start_time=None):
        """Make new route, i.e. thread."""
        threading.Thread.__init__(self)
        self.nut = nut
        self.action = action
        self.start_time = start_time

    def run(self):
        """Start the actual process."""
        if self.action is 'forrage':
            self.nut.collect()
        elif self.action is 'newborn':
            self.nut.new_collection(self.start_time)


def testfunc():
    logging.info('Tetsing')
