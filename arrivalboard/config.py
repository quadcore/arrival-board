import os
import tomllib


APP_CONFIG = {}
_config_path = ""


def init_config(config_path: str, app_config_filename: str):
    """Initialize the application config and fully populate the APP_CONFIG dict."""
    global _config_path
    _config_path = config_path

    app_config_path = os.path.join(_config_path, app_config_filename)
    with open(app_config_path, "rb") as c:
        data = tomllib.load(c)
        APP_CONFIG.update(data)

    if APP_CONFIG["datasources"]["adsb"] == "opensky":
        _init_opensky()
    else:
        raise ValueError("No valid ADSB source specified.")


def _init_opensky():
    try:
        APP_CONFIG["opensky"]["base_url"]
    except KeyError:
        raise ValueError("Invalid OpenSky configuration.")

    try:
        opensky_auth_filename = APP_CONFIG["opensky"]["auth_file"]
        opensky_auth_path = os.path.join(_config_path, opensky_auth_filename)
        with open(opensky_auth_path, "rb") as c:
            data = tomllib.load(c)
            APP_CONFIG["opensky"].update(data)
    except KeyError:
        pass
