from pydantic import Field
from typing import Any, Union, Optional
from .models import PrivateModel

class Callback(PrivateModel):
    ''' The Callback class is used to execute a function after a specified delay '''

    method: str = Field(description='the name of the method to call when the callback is executed')
    seconds: int = Field(exclude=True, default=0, description='the number of seconds to delay before callback is executed')

    def __init__(self, method:Union[str,callable], seconds:Optional[int]=0):
        ''' Initializes the Callback object
        
        Args:
            method: method or method name to call
            seconds: number of seconds to delay before method is executed
        '''

        # if method is a string we can use it directly, otherwise use the name of the callable
        method = method if isinstance(method, str) else method.__name__
        super().__init__(method=method, seconds=seconds)

    def execute(self, instance:object, *args, **kwargs) -> Any:
        ''' Executes the callback on the given instatnce
        
        Args:
            instance: the object whose method we will call
            *args: list of arguments to pass to the method
            **kwargs: list of keyword arguments to pass to the method

        Returns:
            whatever the instance method returns
        '''

        # find the instance method and call it
        return getattr(instance, self.method)(*args, **kwargs)
