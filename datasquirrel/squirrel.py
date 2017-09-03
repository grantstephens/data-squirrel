
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

    def __init__(self, wanted_nuts, data_dir=None, auth_file=None):
        """Get up squirrel."""
        super(Squirrel, self).__init__(data_dir)
        self.log.info('Squirrel awoken!')
        if data_dir is not None:
            self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(os.path.dirname(self.data_dir))
            self.log.info(
                'Path did not exist. Created: {}'.format(
                    os.path.dirname(self.data_dir))
                )
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
            start_time = time.time()-(86400*1)
        self.log.info('Newbord Collection starting from: {}'.format(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))))
        for nut_name, nut in self.nuts.items():
            nut.new_collection(start_time)
            self.log.info('Started new collection of {}'.format(nut_name))

    def forrage(self):
        """Go get more data. Get ALL the Data!."""
        for nut_name, nut in self.nuts.items():
            nut.collect()
        self.log.info('Finished forraging. Going back to sleep')
