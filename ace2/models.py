from __future__ import annotations
from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules
from pydantic import BaseModel, Field
import re
import sys
from typing import Any
from yaml import safe_load

from .utility import camel_to_snake

def find(name:str, base:type) -> dict:
    ''' recursively finds all subclasses in module

    Args:
        name: the name of the module to search
        base: the base class to search for subclasses of

    Returns:
        a mapping of attribute name to attribute of the found subclasses
    '''

    subclasses = {}
    module = sys.modules[name]
    package_dir = Path(module.__file__).resolve().parent
    module_names = sorted([m for (_, m, _) in iter_modules([package_dir])])
    for module_name in module_names:
        sub_module_name = f'{module.__name__}.{module_name}'
        try:
            sub_module = import_module(sub_module_name)
        except ModuleNotFoundError:
            continue
        subclasses.update(find(sub_module_name, base))
        for attribute_name in dir(sub_module):
            attribute = getattr(sub_module, attribute_name)
            if isclass(attribute) and attribute != base and issubclass(attribute, base):
                subclasses[attribute_name] = attribute
    return subclasses

class Private():
    ''' container class for model's private attributes '''

    def __getattr__(self, name:str) -> Any:
        ''' changes get_attribute behavior to return None if the attribute does not exist

        Args:
            name: the name of the attribute to get

        Returns:
            The attribute value or None if the attribute does not exist
        '''

        # return the attribute if it exists
        if name in self.__dict__:
            return self.__dict__[name]

        # return None if the attribute does not exist
        return None

class PrivateModel(BaseModel):
    ''' BaseModel with a private slot for storing private attributes '''

    # pydantic uses slots to have attributes that are not in the model
    __slots__ = ('private',)

    def __init__(self, **kwargs):
        ''' initializes the Model with a private attribute for storing private attributes
        
        Args:
            **kwargs: key word arguments to pass through
        '''

        # init the model
        super().__init__(**kwargs)

        # add the private attribute for storing private attributes
        object.__setattr__(self, 'private', Private())

model_types = {}
class TypedModel(PrivateModel):
    ''' Model class that allows for polymorphic subclass loading '''

    type: str = Field(description='the type string used to identify sub types')

    def __new__(cls, *args, type:Optional[str]=None, **kwargs) -> TypedModel:
        ''' Uses type to construct the correct subclass if one is registered, otherwise constructs the current class

        Args:
            *args: arguments to pass through
            **kwargs: key word arguments to pass through

        Returns:
            the new TypedModel object
        '''

        # get the subclass based on passed in type
        if type:
            cls = model_types.get(cls.base().__name__, {}).get(type, cls)

        # construct an instance of the desired class
        return super().__new__(cls)

    def __init__(self, type:Optional[str]=None, **kwargs):
        ''' intializes the TypedModel instance. Adding type if none was passed in '''

        # set type if none was passed explicitly
        type = self.type if type is None else type
        super().__init__(type=type, **kwargs)

    def __init_subclass__(cls):
        ''' maps all subclasses using the type value so they can be found when constructing new instances '''

        # find the base type
        base = cls.base()

        # skip type registration if this is the base class
        if base == cls:
            return

        # use the class name as the type
        cls.type = camel_to_snake(cls.__name__)

        # add a mapping dictionary for this base type if it does not already exist
        if base.__name__ not in model_types:
            model_types[base.__name__] = {}

        # map subclass to the type string but with a constructor that we can use for loading from a dict
        model_types[base.__name__][cls.type] = type(
            cls.__name__,
            (cls,), 
            {
                '__init__': base.__init__,
                '__init_subclass__': lambda x : None, # NOTE: prevents infinite recursion loop registering new class
            }
        )

    @classmethod
    def base(cls) -> Type[TypedModel]:
        ''' recursviely walks the base classes to find the base model that directly subclasses TypeModel

        Returns:
            the base class that directly subclasses TypeModel
        '''

        for base in cls.__bases__:
            if base == TypedModel:
                return cls
            base = base.base()
            if base:
                return base
        return None
