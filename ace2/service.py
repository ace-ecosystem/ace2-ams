from __future__ import annotations
from boto3.session import Session
from inspect import ismethod
import json
import os
from pydantic import Field
from typing import Optional, Union
import sys

from . import queue
from .models import PrivateModel, TypedModel
from .secrets import get_secret


class Service(TypedModel):
    ''' Base class for making services '''

    instance: Optional[str] = Field(default=None, description='the instance name to load from settings')

    def __init_subclass__(cls):
        ''' Modify all Service subclasses '''
        
        # expose run function so aws lambda functions can find it
        sys.modules[cls.__module__].run = cls.run

        # init base subclasses
        super().__init_subclass__()

    class Settings(PrivateModel):
        ''' base service settings class. Subclasses can override this to define their settings fields '''
        
        @classmethod
        def load(cls, service:str, instance:Optional[str]) -> Service.Settings:
            ''' loads the settings for a given service instance

            Args:
                service: the name of the service to load settings for
                instance: the instance of the service to load settings for

            Returns:
                the loaded settings
            '''

            # load settings from service instance secret
            secret_id = service + '_' + instance if instance else service
            return cls(**json.loads(get_secret(secret_id)))

    @property
    def settings(self) -> Service.Settings:
        ''' the loaded analysis settings '''

        # load settings into cache if we need to
        if self.private.settings == None:
            self.private.settings = self.Settings.load(self.type, self.instance)

        # returned loaded settings
        return self.private.settings

    @classmethod
    def run(cls, event:dict, context:dict):
        ''' AWS lambda function handler that runs a command

        Args:
            event: the aws event message containing the command dict state
            context: aws runtime context (we do not use this)
        '''

        # get the message
        message = event['Records'][0]

        # run the command
        Command(**json.loads(message['body'])).invoke()

        # delete the message
        queue.remove(cls.type, message['receiptHandle'])


class Command(PrivateModel):
    ''' message for telling service what to do '''

    service: Service = Field(description='dict state of the service which will run the method')
    method: str = Field(description='the name of the method to run')
    args: Optional[list] = Field(default_factory=list, description='list of args to pass to method')
    kwargs: Optional[dict] = Field(default_factory=dict, description='list of kwargs to pass to method')

    @classmethod
    def from_method(cls, method) -> Command:
        return cls(
            service = method.__self__,
            method = method.__name__,
        )

    @classmethod
    def send(cls, command:Union[callable,dict], *args, delay:int=0, **kwargs):
        ''' sends the command to the service

        Args:
            command: the service method or command dictionary to send
            *args: positional arguments to pass to the command
            delay: seconds to wait before executing the command
            **kwargs: key word arguments to pass to the command
        '''

        # turn command into a Command object
        if ismethod(command):
            command = cls.from_method(command)
        else:
            command = cls(**command)

        # convert method args/kwargs into commands
        def serialize(value):
            if ismethod(value):
                return cls.from_method(value)
            return value

        # add args
        for arg in args:
            command.args.append(serialize(arg))

        # add kwargs
        for key, value in kwargs.items():
            command.kwargs[key] = serialize(value)

        # queue the command
        queue.add(command.service.type, command.dict(), delay=delay)

    def invoke(self):
        ''' runs the instruction '''

        # get the method from the service
        method = getattr(self.service, self.method)

        # invoke the method
        method(*self.args, **self.kwargs)
