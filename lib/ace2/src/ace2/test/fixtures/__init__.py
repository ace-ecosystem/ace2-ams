from inspect import isfunction, isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

# iterate through the modules in the current package
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([package_dir]):

    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        # add all mock functions
        if attribute_name.startswith('mock_'):
            attribute = getattr(module, attribute_name)

            if isfunction(attribute):
                globals()[attribute_name] = attribute
