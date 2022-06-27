from pydantic import Field
from pydantic.fields import ModelField
from typing import List, Optional, Type

from .models import PrivateModel
from .observables import Observable
from .service import Service
from .database import Database

class Analysis(Service):
    ''' Base Analysis class for building ICE2 analysis '''

    id: int = Field(description='the id of the analysis in the database')
    target: Observable = Field(description='the observable that the analysis is performed on')
    status: Optional[str] = Field(default='running', description='the status of the analysis')
    summary: Optional[str] = Field(default=None, description='the analysis summary to display in the GUI')
    observables: Optional[List[Observable]] = Field(default_factory=list, description='the child observables')
    state: Optional[dict] = Field(default_factory=dict, description='non analysis data storage space')

    class Settings(Service.Settings):
        ''' Base analysis settings class '''
        
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

    def start(self):
        ''' This is the entry point for running analysis '''

        # stop and mark analysis as ignored if it should not run
        if not self.should_run():
            self.status = 'ignored'
            Database().submit_analysis(self)
            return

        # execute the analysis
        self.execute()

    def should_run(self) -> bool:
        ''' Subclasses must override this function to determine when analysis will run

        Returns:
            True if analysis should run
        '''

        raise NotImplementedError()

    def execute(self):
        ''' Subclasses must override this function to perform their analysis '''

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

    def submit(self):
        ''' submits the analysis to the database service '''

        # mark analysis complete and submit to the database
        self.status = 'complete'
        Database().submit_analysis(self)
