
import logging
import os
import time

from . import utils
from .btcc import BTCCCollector
from .googlefinance import GFCollector
from .luno import LunoCollector
from .utils import BaseClass


class Squirrel(BaseClass):
    """Data Squirrel."""

    def __init__(self, wanted_nuts=[], data_dir=None, auth_file=None):
        """Get up squirrel."""
        super(Squirrel, self).__init__(data_dir)
        self.log.info('Squirrel awoken!')
        if data_dir is not None:
            self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
            self.log.info(
                'Path did not exist. Created: {}'.format(self.data_dir)
                )
        if not wanted_nuts:
            wanted_nuts = []
            for fn in os.listdir(self.data_dir):
                if fn.endswith('.h5'):
                    wanted_nuts.append(fn.split('_')[0])
            if not wanted_nuts:
                self.log.exception('No nuts found or given')
                raise IOError('No nuts found or given')
        self.nuts = {}
        if 'luno' in wanted_nuts:
            self.nuts['luno'] = LunoCollector(self.data_dir, None, auth_file)
            wanted_nuts.remove('luno')
        if 'btcc' in wanted_nuts:
            self.nuts['btcc'] = BTCCCollector(self.data_dir, None, auth_file)
            wanted_nuts.remove('btcc')
        for wanted_nut in wanted_nuts:
            self.nuts[wanted_nut] = GFCollector(wanted_nut.upper(),
                                                self.data_dir)

    def newborn(self, start_time=None):
        """Start a new set of collections."""
        if start_time is None:
            start_time = time.time()-(3600*20)
        self.log.info('Newbord Collection starting from: {}'.format(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))))
        for nut_name, nut in self.nuts.items():
            self.log.info('Starting new collection of {}'.format(nut_name))
            nut.new_collection(start_time)
        self.log.info('Newborn born- Yay!')

    def forrage(self):
        """Go get more data. Get ALL the Data!."""
        for nut_name, nut in self.nuts.items():
            nut.collect()
        self.log.info('Finished forraging. Going back to sleep')
