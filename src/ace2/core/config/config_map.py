from pydantic import BaseModel
from pydantic.fields import ModelField

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

        # use class name minus Config on the end as the field name
        name = type.__name__
        if name.endswith('Config'):
            name = name[:-len('Config')]

        # add the field
        cls.__fields__[name] = ModelField.infer(
            name = name,
            value = default,
            annotation = type,
        )
