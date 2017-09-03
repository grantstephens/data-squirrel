import json
import logging
import os
import time

import pandas as pd

from . import utils
from .btcc import BTCCCollector
from .googlefinance import GFCollector
from .luno import LunoCollector
from .utils import BaseClass

logger = logging.getLogger(__name__)


class Squirrel(BaseClass):
    """Data Squirrel."""

    def __init__(self, data_dir=None, auth_file=None):
        super(Squirrel, self).__init__()
        if data_dir is not None:
            self.data
        luno_col = LunoCollector(data_dir, None, auth_file)
        btcc_col = BTCCCollector(data_dir, None, auth_file)
        usdzar_col = GFCollector('USDZAR', data_dir)
