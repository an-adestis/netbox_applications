# Add your plugins and plugin settings here.
# Of course uncomment this file out.

# To learn how to build images with your required plugins
# See https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins

PLUGINS = [
    #"netbox_bgp",
    "adestis_netbox_applications",
    "adestis_netbox_certificate_management",
    # "adestis_netbox_plugin_account_management",
    # "netbox_data_flows"
]

PLUGINS_CONFIG = {
    "adestis_netbox_applications": {},
    # "adestis_netbox_plugin_account_management": {},
    # "netbox_bgp": {},
    # "netbox_data_flows": {}
}
