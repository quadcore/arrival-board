import pytest

from arrivalboard import config


class TestInitConfig:

    def test_initializes_app_config_opensky(self):
        self._init("arrivalboard-opensky.toml")

        expected = {
            'datasources': {
                'adsb': {
                    'opensky': {'base_url': 'https://opensky/test', 'auth_file': 'tests/config/opensky_auth.toml', 'credentials': {'username': 'test-username', 'password': 'test-password'}}
                }, 
                'airports': {
                    'toml': {'folder': '../airdsb-airport-config/toml/'}
                }
            }
        }
        
        assert config.APP_CONFIG == expected
        

    def test_initializes_app_config_opensky_without_auth(self):
        self._init("arrivalboard-opensky-noauth.toml")

        expected = {
            'datasources': {
                'adsb': {
                    'opensky': {'base_url': 'https://opensky/test'}
                }, 
                'airports': {
                    'toml': {'folder': '../airdsb-airport-config/toml/'}
                }
            }
        }
        
        assert config.APP_CONFIG == expected

    def test_raises_error_for_nonexistent_opensky_auth_file(self):
        with pytest.raises(FileNotFoundError):
            self._init("arrivalboard-invalid-opensky-auth.toml")

    def _init(self, config_filename: str):
        config.init_config(f"tests/config/{config_filename}")
