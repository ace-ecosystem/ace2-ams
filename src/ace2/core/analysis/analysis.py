from pydantic import BaseModel, Field
from typing import List, Optional, Type
import sys
from .. import config
from ..callback import Callback
from ..observables import Observable
from ..utility.polymorphism import TypedModel

class Analysis(TypedModel):
    ''' Base Analysis class for building ICE2 analysis '''

    id: int = Field(description='the id of the analysis in the database')
    target: Observable = Field(description='the observable that the analysis is performed on')
    summary: Optional[str] = Field(default=None, description='the analysis summary to display in the GUI')
    details: Optional[dict] = Field(default_factory=dict, description='the analysis details')
    observables: Optional[List[Observable]] = Field(default_factory=list, description='the child observables')
    state: Optional[dict] = Field(default_factory=dict, description='non analysis data storage space')
    callback: Optional[Callback] = Field(
        default = Callback('execute'),
        description='callback to execute when running analysis. If None then analysis is complete'
    )

    class Config(BaseModel):
        ''' Subclasses can override the config class to add new config fields '''
        pass

    @classmethod
    def run(cls, state:dict, context:dict) -> dict:
        ''' AWS Lambda function handler for running the analysis

        Args:
            state (dict): the current analysis state
            context (dict): the context object passed from AWS

        Returns:
            dict: the updated analysis state
        '''

        # load the analysis from the analysis state
        self = cls(**state)

        # call the current callback function which then tells us what to execute after that
        self.callback = self.callback.execute(self, self.target)

        # submit analysis if complete
        if self.callback is None:
            analysis = self.dict(exclude={'callback', 'state'})
            # TODO: submit the analysis excluding callback and state

        # return the dictionary representation of the analysis
        return self.dict()

    @property
    def config(self):
        ''' property shortcut for getting the analysis config from the global config '''

        # load config into cache if we need to
        if self.private.config == None:
            self.private.config = type(self).Config(**config.load()['analysis'][type(self).__name__])

        # returned loaded config
        return self.private.config

    def add(self, observable_type:Type[Observable], *args, **kwargs) -> Observable:
        ''' Adds an observable to the analysis. If the observable is already in the analysis then the metadata is merged

        Args:
            observable_type (Type[Observable]): the class of the observable to add
            *args: the args to pass to the observable constructor
            *kwargs: the keyword args to pass to the observable constructor

        Returns:
            Observable: the added observable
        '''

        # create the observable
        observable = observable_type(*args, **kwargs)

        # add the observable if it is not already in the observables dict
        if observable not in self.observables:
            self.observables.append(observable)
            return observable

        # otherwise return the exiting observable
        return self.observables[self.observables.index(observable)]

    def should_run(self, observable:Observable) -> bool:
        ''' returns True if the analysis should run on the observable, False otherwise

        Args:
            observable (Observable): the observable we are checking to see if we run on

        Returns:
            bool: True if we should run
        '''

        # TODO: default behavior should check required observables and required directives
        raise NotImplementedError()

    def execute(self, observable:Observable) -> Optional[Callback]:
        ''' This is the entry point for running analysis. Subclasses must override this function.

        Args:
            observable (Observable): the target observable to run analysis on

        Returns:
            Callback (optional): The callback to continue analysis or None if analysis is complete
        '''

        raise NotImplementedError()
