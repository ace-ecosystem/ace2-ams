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
            type (str): the type of observable to init
            value (str): the value of the observable
        '''

        # pass type and value to super class as kwargs
        super().__init__(type=type, value=value, **kwargs)

    def __eq__(self, other:Observable) -> bool:
        ''' returns True if other represents the same observable as self

        Args:
            other (Observable): the observanle to compare with self

        Returns:
            bool: True if other is the same observable as self
        '''

        # consider observables equal if they have matching type and matching value
        return self.type == other.type and self.value == other.value

    @property
    def key(self):
        ''' observable key property

        Returns:
            str: the observable key
        '''

        # make key from type and value
        return f'{self.type}|{self.value}'

    def add(self, metadata_type:Type[Metadata], *args, **kwargs):
        ''' adds metadata to the observable

        Args:
            metadata_type (Type[Metadata]): the metadata class to create
            *args: positional arguments to pass to the metadata class
            **kwargs: key word arguments to pass to the metadata class
        '''

        # instantiate the metadata object
        metadata = metadata_type(*args, **kwargs)

        # add the metadata if it is not already in the list of metadata
        if metadata not in self.metadata:
            self.metadata.append(metadata)

    def get_metadata_by_type(self, metadata_type:Type[Metadata]):
        ''' returns list of all metadata in observables metadata with matching metadata_type

        Args:
            metadata_type (Type[Metadata]): the type of metadata to find

        Returns:
            List[Metadata]: the list of metadata in observable with matching metadata_type
        '''

        # filter observables metadata list to just the metadata of type metadata_type
        return [metadata.value for metadata in self.metadata if isinstance(metadata, metadata_type)]

    @property
    def tags(self):
        ''' property that returns all tags in the observables metadata

        Returns:
            list: every Tag in the observables metadata
        '''

        # get all metadata in observable with type of Tag
        return self.get_metadata_by_type(Tag)

    @property
    def display_value(self) -> str:
        ''' gets the first display value for the observable from the metadata. If there is not display value set then
        the observable value is used.

        Returns:
            str: the display value of the object
        '''

        # find all display value metadata
        display_values = self.get_metadata_by_type(DisplayValue)

        # if there is at least one display value metadata then return the first one
        if display_values:
            return display_values[0]

        # if there is no display value set then use the observable value for display
        return self.value
