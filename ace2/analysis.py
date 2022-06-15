from __future__ import annotations
import os
from pydantic import Field
from pydantic.fields import ModelField
from typing import List, Optional, Type

from . import queue
from .config import Config
from .observables import Observable
from .models import TypedModel, PrivateModel
from .service import Service

class Analysis(Service):
    ''' Base Analysis class for building ICE2 analysis '''

    id: int = Field(description='the id of the analysis in the database')
    target: Observable = Field(description='the observable that the analysis is performed on')
    summary: Optional[str] = Field(default=None, description='the analysis summary to display in the GUI')
    observables: Optional[List[Observable]] = Field(default_factory=list, description='the child observables')
    state: Optional[dict] = Field(default_factory=dict, description='non analysis data storage space')

    class Config(Config):
        ''' Base analysis config class '''
        
        cache_seconds: Optional[int] = Field(default=None, description='number of seconds until analysis expires')

    class Details(PrivateModel):
        ''' Base analysis details class '''
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

        # init base subclasses
        super().__init_subclass__()

    @property
    def should_run(self) -> bool:
        ''' True if the analysis condition passes '''
        
        # create shorthand for condition
        target = self.target

        # load the condition
        with open(os.path.join(os.environ['ACE2'], 'services', self.type, 'condition')) as f:
            condition = f.read()

        # evaluate the condition
        return eval(condition)

    def execute(self):
        ''' This is the entry point for running analysis. Subclasses must override this function.

        Args:
            observable: the target observable to run analysis on
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
