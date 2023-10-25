import tomllib


APP_CONFIG = {}


def init():
    _init_app()

    if APP_CONFIG["datasources"]["adsb"] == "opensky":
        _init_opensky()
    else:
        raise ValueError("No valid ADSB source specified.")


def _init_app():
    with open("config/arrivalboard.toml", "rb") as c:
        data = tomllib.load(c)
        APP_CONFIG.update(data)


def _init_opensky():
    try:
        APP_CONFIG["opensky"]["base_url"]
    except KeyError:
        raise ValueError("Invalid OpenSky configuration.")

    try:
        with open("config/opensky_auth.toml", "rb") as c:
            data = tomllib.load(c)
            APP_CONFIG["opensky"].update(data)
    except FileNotFoundError:
        pass
