
import logging
import logging.config
from . import utils

__author__ = 'Grant Stephens'
__email__ = 'grant@stephens.co.za'
__version__ = '0.0.1'

logging.config.fileConfig(utils.LIB_DIR + '/logging.ini')

logger = logging.getLogger(__name__)
