from __future__ import annotations
import os
from os import environ
from typing import Optional
from yaml import safe_load
from .models import PrivateModel

class Settings(PrivateModel):
    ''' base class for building settings models '''

    @classmethod
    def load(cls, path:str, section:Optional[str]=None) -> Settings:
        ''' loads the settings located at path

        Args:
            path: the path to the settings yaml parent directory
            section: when set, loads a specific section in the settings instead of all the sections

        Returns:
            the loaded settings object
        '''

        # load settings yaml into settings object
        with open(os.path.join(environ['ACE2'], path, 'settings.yml')) as f:
            settings_dict = safe_load(f.read()) or {}
        settings = settings_dict[section] if section else settings_dict
        return cls(**settings)
