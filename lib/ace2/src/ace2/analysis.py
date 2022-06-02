from __future__ import annotations
import json
from pydantic import Field
from pydantic.fields import ModelField
from typing import List, Optional, Type
import sys

from . import config, queue
from .callback import Callback
from .observables import Observable
from .models import TypedModel, PrivateModel

class Analysis(TypedModel):
    ''' Base Analysis class for building ICE2 analysis '''

    id: int = Field(description='the id of the analysis in the database')
    target: Observable = Field(description='the observable that the analysis is performed on')
    summary: Optional[str] = Field(default=None, description='the analysis summary to display in the GUI')
    observables: Optional[List[Observable]] = Field(default_factory=list, description='the child observables')
    state: Optional[dict] = Field(default_factory=dict, description='non analysis data storage space')
    callback: Optional[Callback] = Field(
        default = Callback('execute'),
        description='callback to execute when running analysis. If None then analysis is complete'
    )

    class Config(PrivateModel):
        ''' Subclasses can override the config class to add new config fields '''
        pass

    class Details(PrivateModel):
        ''' Subclasses can override the details class to add new details fields '''
        pass

    def __init_subclass__(cls):
        ''' Modify all subclasses of Analysis '''
        
        # add details field
        cls.__fields__['details'] = ModelField.infer(
            name = 'details',
            annotation = cls.Details,
            value = cls.Details(),
            class_validators = None,
            config = cls.__config__,
        )

        # add run funciton to module so aws lambda can find it
        sys.modules[cls.__module__].run = cls.run

        # init base subclasses
        super().__init_subclass__()

    @property
    def config(self) -> Analysis.Config:
        ''' the loaded analysis config '''

        # load config into cache if we need to
        if self.private.config == None:
            self.private.config = type(self).Config(**config.load()['analysis'][type(self).__name__])

        # returned loaded config
        return self.private.config

    @classmethod
    def run(cls, event:dict, context:dict):
        ''' AWS lambda function handler that runs analysis on the event

        Args:
            event: the aws event message
            context: aws runtime context (we do not use this)
        '''

        # get the message from the event
        message = event['Records'][0]

        # create an analysis object from the message
        self = cls(**json.loads(message['body']))

        # call the current callback function which then tells us what to execute after that
        self.callback = self.callback.execute(self, self.target)

        # if analysis is not complete then push it back onto the analysis queue
        if self.callback:
            queue.add(self.type, self.dict(), delay=self.callback.seconds)

        # if analysis is complete then push it (excluding state info) onto the submission queue
        else:
            queue.add('Submission', self.dict(exclude={'callback', 'state'}))

        # delete original message from the analysis queue
        queue.remove(self.type, message['receiptHandle'])

    def execute(self, observable:Observable) -> Optional[Callback]:
        ''' This is the entry point for running analysis. Subclasses must override this function.

        Args:
            observable: the target observable to run analysis on

        Returns:
            The callback to continue analysis or None if analysis is complete
        '''

        raise NotImplementedError()

    def add(self, observable_type:Type[Observable], *args, **kwargs) -> Observable:
        ''' Adds an observable to the analysis

        Args:
            observable_type: the class of the observable to add
            *args: the args to pass to the observable constructor
            *kwargs: the keyword args to pass to the observable constructor

        Returns:
            the added observable instance
        '''

        # create the observable
        observable = observable_type(*args, **kwargs)

        # add the observable if it is not already in the observables dict
        if observable not in self.observables:
            self.observables.append(observable)
            return observable

        # otherwise return the exiting observable
        return self.observables[self.observables.index(observable)]
