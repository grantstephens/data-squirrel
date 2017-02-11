
import logging
import logging.config
from . import utils
import _version

__version__ = _version.__version__
__version_info__ = _version.__version_info__

__author__ = 'Grant Stephens'
__email__ = 'grant@stephens.co.za'

logging.config.fileConfig(utils.LIB_DIR + '/logging.ini')

logger = logging.getLogger(__name__)
