
import logging
import logging.config

from . import _version
import pkg_resources

__version__ = _version.__version__
__version_info__ = _version.__version_info__

__author__ = 'Grant Stephens'
__email__ = 'grant@stephens.co.za'

logging.config.fileConfig(
    pkg_resources.resource_filename(__name__, 'logging.ini'))

logger = logging.getLogger(__name__)
