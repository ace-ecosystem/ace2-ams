from pydantic import BaseModel
from .config_map import ConfigMap

class AnalysisConfigs(ConfigMap):
    ''' container for AnalysisConfig subclasses '''
    pass

class AnalysisConfig(BaseModel):
    ''' Base class for building new Analysis configs '''

    def __init_subclass__(subclass):
        ''' add all AnalysisConfig subclasses to AnalysisConfigs fields '''

        AnalysisConfigs.add(subclass)
