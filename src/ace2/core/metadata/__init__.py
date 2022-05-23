# expose Metadata base class
from .metadata import Metadata

# expose all Metadata subclasses
from ..utility.polymorphism import find_subclasses
globals().update(find_subclasses(__name__, __file__, Metadata))
