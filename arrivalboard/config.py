import tomllib


APP_CONFIG = {}


def init_config(app_config_filepath: str):
    """Initialize the application config and fully populate the APP_CONFIG dict.

    Keyword arguments:
    app_config_filepath -- the path to the TOML file for the application config
    """
    with open(app_config_filepath, "rb") as c:
        data = tomllib.load(c)
        APP_CONFIG.update(data)

    try:
        APP_CONFIG["datasources"]["adsb"]["opensky"]
        _init_opensky()
    except KeyError:
        pass


def _init_opensky():
    opensky_config = APP_CONFIG["datasources"]["adsb"]["opensky"]

    try:
        with open(opensky_config["auth_file"], "rb") as c:
            data = tomllib.load(c)
            opensky_config.update(data)
    except KeyError:
        # If we can't find an auth_file setting, ignore configuring OpenSky
        # authentication and default to non-authenticated requests.
        pass
