__version__ = "0.0.10"  # type: str

from logging import Logger
from logging import getLogger

from .application import FastAPI
from .responses import error_response
from .responses import success_response

logger: Logger = getLogger(__name__)
