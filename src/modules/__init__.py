# import all Analysis subclasses in the modules directory
from ..analysis import Analysis
from ..models import find
globals().update(find(__name__, Analysis))
