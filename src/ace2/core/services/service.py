from typing import Optional
from .. import config
from ..models import PrivateModel

class Service():
    ''' Base class for making configurable services '''

    class Config(PrivateModel):
        ''' base service config class. Subclasses can override this to define their config fields '''
        pass

    def __init__(self, instance:Optional[str]=None):
        ''' loads the service config

        Args:
            instance: which config instance to use
        '''

        # use service class name as config section
        section = type(self).__name__

        # get raw config dictionary
        _config = config.load()

        # get raw service config dcitionary from section and instance or just section if there is no specific instance
        kwargs = _config[section][instance] if instance else _config[section]

        # load the config model
        self.config = type(self).Config(**kwargs)
