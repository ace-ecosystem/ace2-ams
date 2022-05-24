from yaml import safe_load

# the raw config dictionary or None if it has yet to be loaded
raw_config = None

# the location of the config yaml
path = 'config.yml'

def load() -> dict:
    ''' loads the config yaml if it is not already loaded and returns the raw config dictionary

    Returns:
        the raw config dictionary
    '''

    # load raw config dictionary from yaml if it is not loaded yet
    global raw_config
    if raw_config is None:
        with open(path) as f:
            raw_config = safe_load(f.read()) or {}

    # return raw config dictionary
    return raw_config
