from boto3 import client
from hashlib import sha256
import os

def get_storage_id(path:str) -> str:
    """ returns a storage id for a file used to upload/download files

    Args:
        path: the path to the file to create an id for

    Returns:
        the storage id of the file
    """

    # hash the file in chunks to save memory
    h = sha256()
    with open(path, 'rb') as f:
        while True:
            data = f.read(32768)
            if not data:
                break
            h.update(data)
    return h.hexdigest()

def upload(path:str) -> str:
    ''' uploads the file at path to storage and returns the storage id

    Args:
        path: the local path of the file to upload

    Returns:
        the id used to download the file
    '''

    # get a storage id for the file at path
    storage_id = get_storage_id(path)

    # copy the file to s3
    client('s3').upload_file(path, os.environ['FILE_STORAGE_BUCKET'], storage_id)

    # return the storage id
    return storage_id

def download(storage_id:str) -> str:
    ''' downloads a file from storage and returns the path to the new file

    Args:
        storage_id: the id of the file to download

    Returns:
        the local file path of the downloaded file
    '''

    # copy the file from s3
    client('s3').download_file(os.environ['FILE_STORAGE_BUCKET'], storage_id, storage_id)

    # return the path to the file which is just the storage id
    return storage_id
