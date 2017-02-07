
import os.path

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LIB_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
AUTH_FILE = 'auth.json'
DATA_FILE = 'data.h5'

class BaseClass(object):
    """docstring for """
    def __init__(self):
        self.rootDir = ROOT_DIR
        self.dataDir = DATA_DIR
        self.dataFile = DATA_FILE
        self.authFile = AUTH_FILE
