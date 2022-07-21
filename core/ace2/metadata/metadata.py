from __future__ import annotations
from pydantic import Field
from ..models import TypedModel

class Metadata(TypedModel):
    ''' base metadata class '''

    value: str = Field(description='the value of the metadata')

    def __init__(self, value:str, **kwargs):
        ''' Initializes a metadata object

        Args:
            value: the value of the metadata
            **kwargs: key word arguments to pass through
        '''

        # pass type and value to super class as kwargs
        super().__init__(value=value, **kwargs)

    def __eq__(self, other:Metadata) -> bool:
        ''' determines if two instances of metadata are equal
        
        Args:
            other: the metadata to compare

        Returns:
            True if other is the same as self
        '''

        # equal if type and value match
        return self.type == other.type and self.value == other.value
