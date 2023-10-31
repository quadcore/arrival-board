import pytest

from arrivalboard import config
from arrivalboard.exceptions import ConfigError


class TestInitConfig:

    def test_initializes_app_config_opensky(self):
        self._init("arrivalboard-opensky.toml")

        assert config.APP_CONFIG is not None
        assert config.APP_CONFIG["datasources"]["adsb"] == "opensky"
        assert config.APP_CONFIG["opensky"]["base_url"] == "https://opensky/test"
        assert config.APP_CONFIG["opensky"]["auth_file"] == "opensky_auth.toml"
        assert config.APP_CONFIG["opensky"]["credentials"]["username"] == "test-username"
        assert config.APP_CONFIG["opensky"]["credentials"]["password"] == "test-password"

    def test_initializes_app_config_opensky_without_auth(self):
        self._init("arrivalboard-opensky-noauth.toml")

        assert config.APP_CONFIG is not None
        assert config.APP_CONFIG["opensky"]["base_url"] == "https://opensky/test"
        assert "auth_file" not in config.APP_CONFIG["opensky"]
        assert "credentials" not in config.APP_CONFIG["opensky"]

    def test_raises_error_for_no_adsb_source(self):
        with pytest.raises(ConfigError):
            self._init("arrivalboard-invalid-adsb.toml")

    def test_raises_error_for_invalid_opensky(self):
        with pytest.raises(ConfigError):
            self._init("arrivalboard-invalid-opensky.toml")

    def test_raises_error_for_nonexistent_opensky_auth_file(self):
        with pytest.raises(FileNotFoundError):
            self._init("arrivalboard-invalid-opensky-auth.toml")

    def _init(self, config_filename: str):
        config.init_config("tests/config", config_filename)
