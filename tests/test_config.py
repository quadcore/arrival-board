import unittest

from arrivalboard import config


class TestConfig(unittest.TestCase):

    def test_initializes_app_config_opensky(self):
        self._init("arrivalboard-opensky.toml")
        
        self.assertIsNotNone(config.APP_CONFIG)
        self.assertEqual("opensky", config.APP_CONFIG["datasources"]["adsb"])
        self.assertEqual("https://opensky/test", config.APP_CONFIG["opensky"]["base_url"])
        self.assertEqual("opensky_auth.toml", config.APP_CONFIG["opensky"]["auth_file"])
        self.assertEqual("test-username", config.APP_CONFIG["opensky"]["credentials"]["username"])
        self.assertEqual("test-password", config.APP_CONFIG["opensky"]["credentials"]["password"])

    def test_initializes_app_config_opensky_without_auth(self):
        self._init("arrivalboard-opensky-noauth.toml")

        self.assertIsNotNone(config.APP_CONFIG)
        self.assertEqual("https://opensky/test", config.APP_CONFIG["opensky"]["base_url"])
        self.assertFalse("auth_file" in config.APP_CONFIG["opensky"])
        self.assertFalse("credentials" in config.APP_CONFIG["opensky"])

    def test_raises_error_for_no_adsb_source(self):
        with self.assertRaises(ValueError):
            self._init("arrivalboard-invalid-adsb.toml")

    def test_raises_error_for_invalid_opensky(self):
        with self.assertRaises(ValueError):
            self._init("arrivalboard-invalid-opensky.toml")

    def test_raises_error_for_nonexistent_opensky_auth_file(self):
        with self.assertRaises(FileNotFoundError):
            self._init("arrivalboard-invalid-opensky-auth.toml")

    def _init(self, config_filename: str):
        config.init_config("tests/config", config_filename)
