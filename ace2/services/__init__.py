import builtins
from types import ModuleType

from ..service import Service
from ..models import find

# create a dummy module to use in place of modules we do not have installed
class DummyModule(ModuleType):
    # support wildcard imports
    __all__ = [] 

    def __getattr__(self, key):
        return None

# save copy of real import function
realimport = builtins.__import__

def tryimport(name, globals={}, locals={}, fromlist=[], level=-1):
    # try to import the real module
    try:
        return realimport(name, globals, locals, fromlist, level)

    # return a dummy module with the same name if we are unable to import the real one
    except ImportError:
        return DummyModule(name)

# replace import function with try import
builtins.__import__ = tryimport

# import all service header files
# we won't be able to run these directly but we can use them to dispatch instructions
globals().update(find(__name__, Service))

# fix import function
builtins.__import__ = realimport
