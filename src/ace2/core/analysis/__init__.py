# expose Analysis base class
from .analysis import Analysis

# expose all Analysis subclasses
from ..utility.polymorphism import find_subclasses
globals().update(find_subclasses(__name__, __file__, Analysis))
