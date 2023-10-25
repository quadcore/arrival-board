import tomllib


APP_CONFIG = {}


def init():
    _init_opensky()

def _init_opensky():
    with open("config/opensky.toml", "rb") as f:
        data = tomllib.load(f)
        APP_CONFIG["opensky"] = data

    with open("config/opensky_auth.toml", "rb") as f:
        data = tomllib.load(f)
        APP_CONFIG["opensky"].update(data)
