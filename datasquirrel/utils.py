
import os.path

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DATA_FILE = 'histData.h5'
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
AUTH_FILE = 'auth.json'
WALLET_FILE = 'wallet.h5'
DFLOG_FILE = 'tradedLog.h5'


class BaseClass(object):
    """docstring for """
    def __init__(self):
        self.rootDir = ROOT_DIR
        self.dataDir = DATA_DIR
        self.dataFile = DATA_FILE
        self.authFile = AUTH_FILE
        self.walletFile = WALLET_FILE
        self.dfLogFile = DFLOG_FILE
