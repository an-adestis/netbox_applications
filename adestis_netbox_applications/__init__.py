from netbox.plugins import PluginConfig

class AdestisApplicationsConfig(PluginConfig):
    name = 'adestis_netbox_applications'
    verbose_name = 'Applications'
    description = 'A NetBox plugin for managing applications.'
    version = '1.0.2'
    author = 'ADESTIS GmbH'
    author_email = 'pypi@adestis.de'
    base_url = 'applications'
    required_settings = []
    default_settings = {
        'top_level_menu' : True,
    }

config = AdestisApplicationsConfig
