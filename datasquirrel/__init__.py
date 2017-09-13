
import logging
import logging.config
import os
from . import _version
import pkg_resources

__version__ = _version.__version__
__version_info__ = _version.__version_info__

__author__ = 'Grant Stephens'
__email__ = 'grant@stephens.co.za'
ROOT_DIR = os.path.join(
    os.path.dirname(
        pkg_resources.resource_filename(__name__, 'utils.py'))
    , '..')
logging.config.fileConfig(
    pkg_resources.resource_filename(__name__, 'logging.ini'),
    defaults={'logfilename': os.path.join(ROOT_DIR, 'logs',
                                          'datasquirrel.log')})

logger = logging.getLogger(__name__)
