from __future__ import annotations
from inspect import ismethod
import json
import os
from pydantic import Field
from typing import Dict, List, Optional, Union, get_type_hints
import sys

from . import queue
from .models import PrivateModel, TypedModel
from .settings import Settings


class Service(TypedModel):
    ''' Base class for making services '''

    instance: Optional[str] = Field(default=None, description='the instance name to load from settings')

    def __init_subclass__(cls):
        ''' Modify all Service subclasses '''
        
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

    @classmethod
    def run(cls, event:dict, context:dict):
        ''' AWS lambda function handler that runs an instruction

        Args:
            event: the aws event message containing the instruction dict state
            context: aws runtime context (we do not use this)
        '''

        # get the message
        message = event['Records'][0]

        # run the instruction
        Instruction(**json.loads(message['body'])).invoke()

        # delete the message
        queue.remove(cls.type, message['receiptHandle'])


class Instruction(PrivateModel):
    ''' message for telling service what to do '''

    service: Service = Field(description='dict state of the service which will run the method')
    method: str = Field(description='the name of the method to run')
    args: Optional[List] = Field(default_factory=list, description='list of args to pass to method')
    kwargs: Optional[Dict] = Field(default_factory=dict, description='list of kwargs to pass to method')

    @classmethod
    def from_method(cls, method) -> Instruction:
        return Instruction(
            service = method.__self__.dict(),
            method = method.__name__,
        )

    @classmethod
    def send(cls, instruction:Union[callable,dict], *args, delay:int=0, **kwargs):
        ''' sends the instruction to the service

        Args:
            instruction: the service method or instruction diction to send
            *args: positional arguments to pass to the instruction
            delay: seconds to wait before executing the instruction
            **kwargs: key word arguments to pass to the instruction
        '''

        # turn instruction into an Instruciton object
        instruction = cls.from_method(instruction) if ismethod(instruction) else cls(**instruction)

        # method for converting arguments
        def serialize(value):
            # convert methods into instructions
            if ismethod(value):
                return cls.from_method(value)

            # use other values as is
            return value

        # convert all arguments
        for arg in args:
            instruction.args.append(serialize(arg))
        for key, value in kwargs.items():
            instruction.kwargs[key] = serialize(value)

        # queue the instruction
        queue.add(instruction.service.type, instruction.dict(), delay=delay)

    def invoke(self):
        ''' runs the instruction '''

        # get the method from the service
        method = getattr(self.service, self.method)

        # invoke the method
        method(*self.args, **self.kwargs)
