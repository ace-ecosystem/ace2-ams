import datetime
from pydantic import Field, validator
from typing import Union, Optional
from .models import PrivateModel

class Callback(PrivateModel):
    ''' The Callback class is used to execute a function sometime in the future '''

    method: str = Field(description='the name of the method to call when the callback is executed')
    timestamp: datetime.datetime = Field(description='the datetime to execute the callback at')

    def __init__(self, method:Union[str,callable], timestamp:Optional[datetime.datetime]=None, **kwargs):
        ''' Initializes the Callback object
        
        Args:
            method (Union[str, callable]): the method or method name to call
            timestamp (datetime): time when the callback should be called
            **kwargs: if no timestamp is given then kwargs are passed to datetime.timedelta to determine how long to wait
        '''

        # if method is a string we can use it directly, otherwise use the name of the callable
        method = method if isinstance(method, str) else method.__name__

        # if timestamp is present then use it, otherwise create one from kwargs
        timestamp = timestamp if timestamp else datetime.datetime.utcnow() + datetime.timedelta(**kwargs)

        # init the callback
        super().__init__(method=method, timestamp=timestamp)

    class Config:
        ''' pydantic config that sets a json encoder for datetime fields '''

        # specify how to serialize datetime objects
        json_encoders = {
            datetime.datetime: lambda v: v.strftime('%Y-%m-%dT%H:%M:%SZ')
        }

    @validator('timestamp', pre=True)
    def parse_timestamp(cls, value):
        ''' validates and parses the timestamp field 
        
        Args:
            value (str): the serialized timestamp value

        Returns:
            datetime.datetime: the deserialized timestamp value
        '''

        # parse timestamp str into datetime object
        if isinstance(value, str):
            return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        else:
            return value

    def dict(self, *args, **kwargs):
        ''' override the dict function to convert timestamp to a string
        
        Returns:
            dict: the dictionary representation of this object
        '''

        # make the dict form the super class
        d = super().dict(*args, **kwargs)

        # convert timestamp in the dict to str
        d['timestamp'] = d['timestamp'].strftime('%Y-%m-%dT%H:%M:%SZ')

        return d

    def execute(self, instance, *args, **kwargs):
        ''' Executes the callback on the given instatnce
        
        Args:
            instance (object): the object whose method we will call
            *args: list of arguments to pass to the method
            **kwargs: list of keyword arguments to pass to the method
        '''

        # find the instance method and call it
        return getattr(instance, self.method)(*args, **kwargs)
