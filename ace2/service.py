import os
from typing import Optional
from .config import Config
from .utility import camel_to_snake

class Service():
    ''' Base class for making configurable services '''

    class Config(Config):
        ''' base service config class. Subclasses can override this to define their config fields '''
        pass

    def __init__(self, instance:Optional[str]='default'):
        ''' loads the service config

        Args:
            instance: which instance in the config to use
        '''

        # load the config
        self.config = self.Config.load(os.path.join('lib', camel_to_snake(type(self).__name__)), section=instance)
