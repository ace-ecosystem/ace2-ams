from boto3 import resource
from typing import Optional

from .timestamp import Timestamp, fromisoformat

def persistent_data():
    ''' returns the boto3 resource for the persistent data table '''
    return resource('dynamodb').Table('persistent_data')

def get(key:str) -> Optional[str]:
    ''' gets the value for a given key from persistent data

    Args:
        key: the key of the value to get

    Returns:
        the value stored in persistent data with given key or None if the key does not exist
    '''

    # lookup the key in the persistent data table
    response = persistent_data().get_item(
        Key = {
            'key': key,
        },
        AttributesToGet = [
            'value',
        ],
        ConsistentRead = True,
    )

    # return the key's value or None if the key does not exist
    return response['Item']['value'] if 'Item' in response else None

def set(key:str, value:str):
    ''' sets the value for a given key in the persistent data db

    Args:
        key: the key to set the value of
        value: the value to set
    '''

    # store the value in the persistent data table under given key
    persistent_data().put_item(
        Item = {
            'key': key,
            'value': value,
        }
    )

def get_timestamp(key:str, default:Optional[Timestamp]=None) -> Optional[Timestamp]:
    ''' gets a timestamp from persistent data string

    Args:
        key: the key of the timestamp to get
        default: a default timestamp to return if the key is not in persistent data

    Returns:
        the timestamp for given key in persistent data or a default timestamp if key is not found
    '''

    # get the timestamp from persistent data as a string
    timestamp = get(key)

    # convert string to timestamp or return default if not found
    return fromisoformat(timestamp) if timestamp else default

def set_timestamp(key:str, timestamp:Timestamp):
    ''' sets the value of key in persistent data to the isoformatted string value of given timestamp

    Args:
        key: the key to set the value of
        timestamp: the Timestamp object to store
    '''

    # set the key's value in persistent data to the iso formatted string representation of given timestamp
    set(key, timestamp.isoformat())
