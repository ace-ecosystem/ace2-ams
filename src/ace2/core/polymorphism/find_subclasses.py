from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

def find_subclasses(name:str, file:str, base:type) -> dict:
    ''' finds all subclasses of base in module (not recursive)

    Args:
        name (str): the name of the module we are importing from
        file (str): the __init__.py file path to search the parent dir of
        base (type): the base class to search for subclasses of

    Returns:
        dict: a mapping of attribute name to attribute of the found subclasses
    '''

    subclasses = {}
    package_dir = Path(file).resolve().parent
    for (_, module_name, _) in iter_modules([package_dir]):
        module = import_module(f"{name}.{module_name}")
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isclass(attribute) and attribute != base and issubclass(attribute, base):
                subclasses[attribute_name] = attribute
    return subclasses
