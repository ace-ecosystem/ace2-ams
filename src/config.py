from __future__ import annotations
import os
from os import environ
from typing import Optional
from yaml import safe_load
from .models import PrivateModel

class Config(PrivateModel):
    ''' base class for building config models '''

    @classmethod
    def load(cls, path:str, section:Optional[str]=None) -> Config:
        ''' loads the config located at path

        Args:
            path: the path to the config yaml parent directory
            section: when set, loads a specific section in the config instead of all the sections

        Returns:
            the loaded config object
        '''

        # load config yaml into config object
        with open(os.path.join(environ['ACE2'], path, 'config.yml')) as f:
            config_dict = safe_load(f.read()) or {}
        config = config_dict[section] if section else config_dict
        return cls(**config)
