from os.path import basename
from pydantic import Field
from typing import Optional

from .observable import Observable
from ..metadata import *
from .. import storage

class File(Observable):
    ''' Observable that represents a file '''

    def __init__(self, path:str, **kwargs):
        ''' Initializes a file observable

        Args:
            path: the local file path
            **kwargs: key word arguments to pass through
        '''

        # upload the file to storage
        storage_id = storage.upload(path)

        # use the storage id as the value for the observable
        super().__init__(self.type, storage_id, **kwargs)

        # set the local path so we use it instead of downloading another copy
        self.private.path = path

        # use the basename of path as the display value
        self.add(DisplayValue, basename(path))

    @property
    def path(self) -> str:
        ''' the local path to the file. Triggers download of file if it does not exist locally '''

        # download file from storage if we do not have a local copy
        if self.private.path is None:
            self.private.path = storage.download(self.value)

        # return the local path to the file
        return self.private.path
