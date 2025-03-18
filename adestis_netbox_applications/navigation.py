from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu
from netbox.choices import ButtonColorChoices
from django.conf import settings

_applications = [
    PluginMenuItem(
        link='plugins:adestis_netbox_applications:installedapplication_list',
        link_text='Applications',
        permissions=["adestis_netbox_applications.installedapplication_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_applications:installedapplication_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_applications.installedapplication_add"]),
        )
    ),    
]

_software = [
    PluginMenuItem(
        link='plugins:adestis_netbox_applications:software_list',
        link_text='Softwares',
        permissions=["adestis_netbox_applications.software_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_applications:software_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_applications.software_add"]),
        )
    ),    
]

plugin_settings = settings.PLUGINS_CONFIG.get('adestis_netbox_applications', {})

if plugin_settings.get('top_level_menu'):
    menu = PluginMenu(  
        label="Application Management",
        groups=(
            ("Applications", _applications),
            ("Software", _software ),
        ),
        icon_class="mdi mdi-key",
    )
else:
    menu_items = _applications