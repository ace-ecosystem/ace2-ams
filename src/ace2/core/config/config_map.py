from pydantic import BaseModel
from pydantic.fields import ModelField
from ..polymorphism.utility import camel_to_snake

class ConfigMap(BaseModel):
    ''' Base class for creating config sections that are appended to at runtime '''

    @classmethod
    def add(cls, type):
        ''' adds a new field to the model for type

        Args:
            type (Type): the class to add a field for
        '''

        # attempt to create a default value otherwise make the field required
        try:
            default = type()
        except:
            default = ...

        # use snake case of class name as the field name and remove config from end
        name = camel_to_snake(type.__name__)
        if name.endswith('_config'):
            name = name[:-len('_config')]

        # add the field
        cls.__fields__[name] = ModelField.infer(
            name = name,
            value = default,
            annotation = type,
            class_validators = None,
            config = cls.__config__
        )
