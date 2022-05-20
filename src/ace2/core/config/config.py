from pydantic import Field
import yamp
from .config_map import ConfigMap

config = None

class Config(ConfigMap):
    analysis: AnalysisConfigs = Field(description='dict of analysis configs where key is the type of analysis')

def load():
    global config
    with open('config.yml') as f:
        config = Config(**yaml.safe_load(f))
