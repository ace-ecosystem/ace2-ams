from pydantic import Field
from .config_map import ConfigMap

class Config(ConfigMap):
    analysis: AnalysisConfigs = Field(description='dict of analysis configs where key is the type of analysis')
