from __future__ import annotations
from pydantic import Field
from typing import List, Optional
from ..metadata import *
from ..models import TypedModel

class Observable(TypedModel):
    ''' Default observable class '''

    value: str = Field(description='the string value of the observable')
    metadata: Optional[List[Metadata]] = Field(default_factory=list, description="the observables's metadata")

    def __init__(self, type:str, value:str, **kwargs):
        ''' Initializes an observable object.

        Args:
            type: the type of observable to init
            value: the value of the observable
            **kwargs: key word arguments to pass through
        '''

        # pass type and value to super class as kwargs
        super().__init__(type=type, value=value, **kwargs)

    def __eq__(self, other:Observable) -> bool:
        ''' Checks to see if two observables are the same

        Args:
            other: the observable to compare

        Returns:
            True if other is the same observable
        '''

        # consider observables equal if they have matching type and matching value
        return self.type == other.type and self.value == other.value

    @property
    def key(self) -> str:
        ''' key used to identify an observable '''

        # make key from type and value
        return f'{self.type}|{self.value}'

    def add(self, metadata_type:Type[Metadata], *args, **kwargs):
        ''' adds metadata to the observable

        Args:
            metadata_type: the metadata class to create
            *args: positional arguments to pass to the metadata class
            **kwargs: key word arguments to pass to the metadata class
        '''

        # instantiate the metadata object
        metadata = metadata_type(*args, **kwargs)

        # add the metadata if it is not already in the list of metadata
        if metadata not in self.metadata:
            self.metadata.append(metadata)

    def get_metadata_by_type(self, metadata_type:Type[Metadata]) -> List[str]:
        ''' Finds all metadata values for a given metadata type

        Args:
            metadata_type: the type of metadata to find

        Returns:
            the list of metadata values with metadata_type
        '''

        # filter observables metadata list to just the metadata of type metadata_type
        return [metadata.value for metadata in self.metadata if isinstance(metadata, metadata_type)]

    @property
    def tags(self) -> List[str]:
        ''' list of tag values '''

        # get all metadata in observable with type of Tag
        return self.get_metadata_by_type(Tag)

    @property
    def display_value(self) -> str:
        ''' The display value of the observable. If none is set then use the value as the display value '''

        # find all display value metadata
        display_values = self.get_metadata_by_type(DisplayValue)

        # if there is at least one display value metadata then return the first one
        if display_values:
            return display_values[0]

        # if there is no display value set then use the observable value for display
        return self.value
