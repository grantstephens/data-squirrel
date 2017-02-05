
import os.path

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DATA_FILE = 'histData.h5'
LOG_DIR = os.path.join(ROOT_DIR, 'logs')


class BaseClass(object):
    """docstring for """
    def __init__(self):
        self.rootDir = ROOT_DIR
        self.dataDir = DATA_DIR
        self.dataFile = DATA_FILE
