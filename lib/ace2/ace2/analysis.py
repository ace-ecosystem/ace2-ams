from __future__ import annotations
from pydantic import Field
from pydantic.fields import ModelField
from typing import List, Optional, Type, Tuple
import sys

from . import config
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

    class Requirements():
        ''' Subclass can override the requirements class to alter the requirements '''
        observables: Union[str, Type[Observable], Tuple[Union[str,Type[Observable]]]] = ()
        directives: Union[str, Tuple[str]] = ()

    def requirements_met(self) -> bool:
        ''' Determines if the analysis should run

        Returns:
            True if the analysis should run
        '''

        # do not run if the target type is not valid for this analysis
        observables = self.Requirements.observables 
        if not isinstance(self.Requirements.observables, tuple):
            observables = (self.Requirements.observables,)
        if self.target.type not in [t if isinstance(t, str) else t.type for t in observables]:
            return False

        # do not run if the observable is missing a required directive
        directives = self.Requirements.directives 
        if not isinstance(self.Requirements.directives, tuple):
            directives = (self.Requirements.directives,)
        for directive in directives:
            if directive not in self.target.directives:
                return False

        # analysis should run on this target
        return True

    def __init_subclass__(cls):
        ''' Add details field to all subclasses '''
        
        cls.__fields__['details'] = ModelField.infer(
            name = 'details',
            annotation = cls.Details,
            value = cls.Details(),
            class_validators = None,
            config = cls.__config__,
        )

        super().__init_subclass__()

    @property
    def config(self) -> Analysis.Config:
        ''' the loaded analysis config '''

        # load config into cache if we need to
        if self.private.config == None:
            self.private.config = type(self).Config(**config.load()['analysis'][type(self).__name__])

        # returned loaded config
        return self.private.config

    def run(self) -> dict:
        ''' runs the analysis

        Returns:
            the updated analysis state
        '''

        # call the current callback function which then tells us what to execute after that
        self.callback = self.callback.execute(self, self.target)

        # submit analysis if complete
        if self.callback is None:
            analysis = self.dict(exclude={'callback', 'state'})
            # TODO: submit the analysis excluding callback and state

        # return the dictionary representation of the analysis
        return self.dict()

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
