# import all Analysis subclasses in the modules directory
from ..service import Service
from ..models import find
globals().update(find(__name__, Service))
