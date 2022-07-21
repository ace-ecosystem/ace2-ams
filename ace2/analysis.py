from pydantic import Field
from pydantic.fields import ModelField
from typing import List, Optional, Type

from .models import PrivateModel, TypedModel
from .observables import Observable
from .database import Database

class Analysis(TypedModel):
    ''' Base Analysis class for building ICE2 analysis '''

    id: Optional[int] = Field(default=None, description='the id of the analysis in the database')
    target: Optional[Observable] = Field(default=None, description='the observable that the analysis is performed on')
    status: Optional[str] = Field(default='running', description='the status of the analysis')
    summary: Optional[str] = Field(default=None, description='the analysis summary to display in the GUI')
    observables: Optional[List[Observable]] = Field(default_factory=list, description='the child observables')

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

    def ignore(self):
        ''' submits the analysis to the database service with status=ignore '''

        # mark analysis ignored and submit to the database
        self.status = 'ignore'
        Database().submit_analysis(self)

    def submit(self):
        ''' submits the analysis to the database service '''

        # mark analysis complete and submit to the database
        self.status = 'complete'
        Database().submit_analysis(self)
