from os.path import basename
from pydantic import Field
from typing import Optional

from .observable import Observable
from ..metadata import *
from .. import storage

class File(Observable):
    ''' Observable that represents a file '''

    local_path: Optional[str] = Field(exclude=True, default=None, description='the local path of the file')

    def __init__(self, path:str, **kwargs):
        ''' Initializes a file observable

        Args:
            path (str): the local file path
        '''

        # upload the file to storage
        storage_id = storage.upload(path)

        # use the storage id as the value for the observable
        super().__init__(self.type, storage_id, **kwargs)

        # set the local path so we use it instead of downloading another copy
        self.local_path = path

        # use the basename of path as the display value
        self.add(DisplayValue, basename(path))

    @property
    def path(self):
        # download file from storage if we do not have a local copy
        if self.local_path is None:
            self.local_path = storage.download(self.value)

        # return the local path to the file
        return self.local_path
