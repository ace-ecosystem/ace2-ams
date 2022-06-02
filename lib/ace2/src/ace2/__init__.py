from .analysis import Analysis
from .callback import Callback
from .metadata import *
from .observables import *
import logging
if logging.getLogger().handlers:
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger().setFormatter(logging.Formatter(fmt='[%(levelname)s] %(message)s'))
else:
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
