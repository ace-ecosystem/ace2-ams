from __future__ import annotations
from inspect import ismethod
import json
import os
from pydantic import Field
from typing import Dict, List, Optional, Union
import sys

from . import queue
from .config import Config
from .models import PrivateModel, TypedModel

class Instruction(PrivateModel):
    ''' message for telling service what to do '''

    service: dict = Field(description='dict state of the service which will run the method')
    method: str = Field(description='the name of the method to run')
    args: Optional[List] = Field(default_factory=list, description='list of args to pass to method')
    kwargs: Optional[Dict] = Field(default_factory=dict, description='list of kwargs to pass to method')

    def __init__(self, method:Union[dict,callable]):
        ''' initializes and instruciton

        Args:
            method: the instruction dict state or a service method to create an instruction from
        '''

        # create instruction from dict state
        if isinstance(method, dict):
            super().__init__(**method)

        # create instruction from service method
        else:
            super().__init__(
                state = method.__self__.dict(),
                method = method.__name__,
            )

def dispatch(method:Union[dict,callable], *args, delay:Optioanl[int]=0, **kwargs):
    ''' creates an instruction from given service method and sends it to the service

    Args:
        method: the service method or instruction dict state to call
        delay: seconds to wait before running the instruction
        *args: list of args to pass to the instruction
        **kwargs: key word args to pass to the instruction
    '''

    # create the instruction from the given service method or Instruction dictionary state
    instruction = Instruction(method)

    # convert service method args/kwargs to Instrucitons
    for arg in args:
        instruction.args.append(Instruction(arg) if ismethod(arg) else arg)
    for key, value in kwargs:
        instruction.kwargs[key] = Instruction(value) if ismethod(value) else value

    # queue the instruction
    queue.add(instruction.service.type, instruction.dict(), delay=delay)

class Service(TypedModel):
    ''' Base class for making configurable services '''

    instance: Optional[str] = Field(default=None, description='the name of the configured instance')

    def __init_subclass__(cls):
        ''' Modify all subclasses of Service '''
        
        # expose run function so aws lambda functions can find it
        sys.modules[cls.__module__].run = cls.run

        # init base subclasses
        super().__init_subclass__()

    class Config(Config):
        ''' base service config class. Subclasses can override this to define their config fields '''
        pass

    @property
    def config(self) -> Service.Config:
        ''' the loaded analysis config '''

        # load config into cache if we need to
        if self.private.config == None:
            path = os.path.join('services', self.type)
            self.private.config = self.Config.load(path, section=self.instance)

        # returned loaded config
        return self.private.config

    def __getattr__(self, name:str) -> callable:
        ''' return a service method with given name when non existent attributes are fetched.
        This allows other services to dispatch instructions to a service without importing
        the full service class which would require installing that services dependencies.

        Args:
            name: the name of the function

        Returns:
            A service method with the given name
        '''

        def func():
            pass
        func.__self__ = self
        func.__name__ = name
        return func

    @classmethod
    def run(cls, event:dict, context:dict):
        ''' AWS lambda function handler that runs an instruction

        Args:
            event: the aws event message containing the instruction dict state
            context: aws runtime context (we do not use this)
        '''

        # turn dict state of instruction into an Instruction object
        message = event['Records'][0]
        instruction = Instruction(json.loads(message['body']))

        # init the Service object from the Instruction service state
        service = cls(**instruction.service)

        # run the method
        getattr(service, instruction.method)(*instruction.args, **instruction.kwargs)

        # delete original message from the queue
        queue.remove(service.type, message['receiptHandle'])
