from pydantic import Field
from yaml import safe_load
from .config_map import ConfigMap
from .analysis import AnalysisConfigs

class Config(ConfigMap):
    analysis: AnalysisConfigs = Field(
        default_factory=dict,
        description='dict of analysis configs where key is the analysis type'
    )

_config = None
_config_path = 'config.yml'
def CONFIG():
    # load config if it isnt already
    global _config
    if _config is None:
        with open(_config_path) as f:
            _config = Config(**(safe_load(f) or {}))

    # return the loaded config
    return _config
