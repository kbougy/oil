import unittest

from oil import Oil

class OilTestCase(unittest.TestCase):

    def test_providers_are_default_with_no_config_passed(self):
        oil = Oil()
        providers = oil.providers
        self.assertEqual(providers, ['aws'])

    def test_add_config_post_initialization_configures_plugins(self):
        oil = Oil()
        config = {
            'aws': {
                'cloudfront': {
                    'plugins': [
                        {
                            'name': 'tls_protocol'
                        }
                    ]
                }
            }
        }

        oil.configure(config)
        self.assertEqual(oil.config, config)

        plugin = oil.plugins[0]
        self.assertEqual(plugin.name, 'tls_protocol')

    def test_services_throws_error_with_unsupported_provider(self):
        oil = Oil()
        with self.assertRaises(RuntimeError):
            services = oil.services('unsupported_provider')

    def test_services_empty_with_no_services(self):
        config = {
            'aws': {}
        }
        oil = Oil(config)
        with self.assertRaises(RuntimeError):
            services = oil.services('unsupported_provider')

    def test_loading_plugins_throws_error_if_provider_is_not_registered(self):
        config = {
            'unsupported_provider': {
                'this': {
                    'plugins': []
                }
            }
        }

        with self.assertRaises(RuntimeError):
            oil = Oil(config)

    def test_loading_plugins_throws_error_if_service_is_not_registered(self):
        config = {
            'aws': {
                'unsupported_service': {
                    'plugins': []
                }
            }
        }

        with self.assertRaises(RuntimeError):
            oil = Oil(config)

    def test_loading_plugins_throws_error_if_plugin_is_not_registered(self):
        config = {
            'aws': {
                'cloudfront': {
                    'plugins': [
                        {
                            'name': 'fake_plugin'
                        }
                    ]
                }
            }
        }

        with self.assertRaises(RuntimeError):
            oil = Oil(config)
