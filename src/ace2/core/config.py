from yaml import safe_load

_config = None
_config_path = 'config.yml'
def load():
    # load config if it isnt already
    global _config
    if _config is None:
        with open(_config_path) as f:
            _config = safe_load(f.read()) or {}

    # return the loaded config
    return _config
