from __future__ import annotations
from pydantic import Field
from typing import List, Optional, Type
import sys
from .. import config
from ..callback import Callback
from ..observables import Observable
from ..models import TypedModel, PrivateModel

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

    class Config(PrivateModel):
        ''' Subclasses can override the config class to add new config fields '''
        pass

    @property
    def config(self) -> Analysis.Config:
        ''' the analysis config '''

        # load config into cache if we need to
        if self.private.config == None:
            self.private.config = type(self).Config(**config.load()['analysis'][type(self).__name__])

        # returned loaded config
        return self.private.config

    @property
    def valid_observable_types(self) -> List[Union[str,Type[Observable]]]:
        ''' which observable types to run on '''

        return []

    @property
    def required_directives(self) -> List[str]:
        ''' directives the target must have in order to run analysis '''

        return []

    def should_run(self) -> bool:
        ''' Determines if the analysis should run on the observable

        Returns:
            True if the analysis should run
        '''

        # do not run if the target type is not valid for this analysis
        if self.target.type not in [t if isinstance(t, str) else t.type for t in self.valid_observables]:
            return False

        # do not run if the observable is missing a required directive
        for directive in self.required_directives:
            if directive not in self.target.directives:
                return False

        # analysis should run on this target
        return True

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
