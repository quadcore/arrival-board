import os
import tomllib

from arrivalboard.exceptions import ConfigError


APP_CONFIG = {}
_config_path = ""


def init_config(config_path: str, app_config_filename: str):
    """Initialize the application config and fully populate the APP_CONFIG dict.

    Keyword arguments:
    config_path -- the path of the folder that contains the configuration files
    app_config_filename -- the name of the TOML file for the application config
    """
    global _config_path
    _config_path = config_path

    app_config_path = os.path.join(_config_path, app_config_filename)
    with open(app_config_path, "rb") as c:
        data = tomllib.load(c)
        APP_CONFIG.update(data)

    if APP_CONFIG["datasources"]["adsb"] == "opensky":
        _init_opensky()
    else:
        raise ConfigError("No valid ADSB source specified.")


def _init_opensky():
    try:
        APP_CONFIG["opensky"]["base_url"]
    except KeyError:
        raise ConfigError("Missing OpenSky base url.")

    try:
        opensky_auth_filename = APP_CONFIG["opensky"]["auth_file"]
        opensky_auth_path = os.path.join(_config_path, opensky_auth_filename)
        with open(opensky_auth_path, "rb") as c:
            data = tomllib.load(c)
            APP_CONFIG["opensky"].update(data)
    except KeyError:
        # If we can't find an auth_file setting, ignore configuring OpenSky
        # authentication and default to non-authenticated requests.
        pass
