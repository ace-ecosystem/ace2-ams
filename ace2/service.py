from __future__ import annotations
from inspect import ismethod
import json
import os
from pydantic import Field, Extra
from typing import Any, Dict, List, Optional, Type, Union, get_type_hints
import sys

from . import queue
from .settings import Settings
from .models import PrivateModel, TypedModel

class Service(TypedModel, extra=Extra.allow):
    ''' Base class for making services '''

    instance: Optional[str] = Field(default=None, description='the instance name to load from settings')

    def __init__(self, type:str, **kwargs):
        ''' Initializes the service

        Args:
            type: the type of service
            **kwargs: key word arguments to pass through
        '''

        super().__init__(type=type, **kwargs)

    def __init_subclass__(cls):
        ''' Modify all subclasses of Service '''
        
        # expose run function so aws lambda functions can find it
        sys.modules[cls.__module__].run = cls.run

        # init base subclasses
        super().__init_subclass__()

    class Settings(Settings):
        ''' base service settings class. Subclasses can override this to define their settings fields '''
        pass

    @property
    def settings(self) -> Service.Settings:
        ''' the loaded analysis settings '''

        # load settings into cache if we need to
        if self.private.settings == None:
            path = os.path.join('services', self.type)
            self.private.settings = self.Settings.load(path, section=self.instance)

        # returned loaded settings
        return self.private.settings

    def dispatch(self, method:str, *args, delay:int=0, **kwargs):
        ''' sends an instruction to the service

        Args:
            method: the method to run
            *args: positional arguments to pass
            delay: seconds to wait before executing the method
            **kwargs: key word arguments to pass
        '''

        instruction = Instruction(service=self.dict(), method=method)
        instruction.dispatch(*args, delay=delay, **kwargs)

    def convert(self, value:Any, hint:Type) -> Any:
        ''' converts value base on hint

        Args:
            value: the value to convert
            hint: the type hint to convert to

        Returns:
            the converted value
        '''

        # convert Instructions
        if hint == Instruction:
            return Instruction(**value)

        # use the value as is
        return value

    @classmethod
    def run(cls, event:dict, context:dict):
        ''' AWS lambda function handler that runs an instruction

        Args:
            event: the aws event message containing the instruction dict state
            context: aws runtime context (we do not use this)
        '''

        # turn dict state of instruction into an Instruction object
        message = event['Records'][0]
        instruction = Instruction(**json.loads(message['body']))

        # init the Service object from the Instruction service state
        service = cls(**instruction.service)

        # get the method from the service
        method = getattr(service, instruction.method)

        # convert args using hints
        hints = get_type_hints(method)
        arg_hints = list(hints.values())
        for i in range(len(args)):
            args[i] = self.convert(args[i], arg_hints[i])

        for key, value in kwargs.items():
            kwargs[key] = self.convert(value, hints[key])

        # invoke the method
        method(*instruction.args, **instruction.kwargs)

        # delete original message from the queue
        queue.remove(service.type, message['receiptHandle'])

class Instruction(PrivateModel):
    ''' message for telling service what to do '''

    service: Service = Field(description='dict state of the service which will run the method')
    method: str = Field(description='the name of the method to run')
    args: Optional[List] = Field(default_factory=list, description='list of args to pass to method')
    kwargs: Optional[Dict] = Field(default_factory=dict, description='list of kwargs to pass to method')

    def convert(self, value:Any) -> Any:
        ''' converts values into serializable form

        Args:
            value: the value to convert

        Retruns:
            the serilizable value
        '''

        # convert service methods to Instructions
        if ismethod(value):
            return Instruction(
                service = value.__self__.dict(),
                method = value.__name__,
            )

        # use value as is
        return value

    def dispatch(self, *args, delay:int=0, **kwargs):
        ''' sends the instruction to the service

        Args:
            *args: positional arguments to pass to the instruction
            delay: seconds to wait before executing the instruction
            **kwargs: key word arguments to pass to the instruction
        '''

        # convert args
        for arg in args:
            self.args.append(self.convert(arg))
        for key, value in kwargs:
            self.kwargs[key] = self.convert(value)

        # queue the instruction
        queue.add(self.service.type, self.dict(), delay=delay)
