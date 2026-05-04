from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu
from netbox.choices import ButtonColorChoices
from django.conf import settings
from django.utils.translation import gettext_lazy as _

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
        link_text='Software',
        permissions=["adestis_netbox_applications.software_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_applications:software_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_applications.software_add"]),
        )
    ),    
]

_application_types = [
    PluginMenuItem(
        link='plugins:adestis_netbox_applications:installedapplicationtypes_list',
        link_text='Application Types',
        permissions=["adestis_netbox_applications.installedapplicationtypes_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_applications:installedapplicationtypes_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_applications.installedapplicationtypes_add"]),
        )
    ),    
]

_software_version = [
    PluginMenuItem(
        link='plugins:adestis_netbox_applications:softwareversion_list',
        link_text='Software Version',
        permissions=["adestis_netbox_applications.softwareversion_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_applications:softwareversion_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_applications.software_add"]),
        )
    ),    
]

plugin_settings = settings.PLUGINS_CONFIG.get('adestis_netbox_applications', {})

if plugin_settings.get('top_level_menu'):
    menu = PluginMenu(
        label="Application Management",
        icon_class="mdi mdi-application-cog-outline",
        groups=[
            (
                _("Applications"),
                (
                    _applications[0],
                    _application_types[0],
                )
            ),
            (
                _("Software"),
                (
                    _software[0],
                    _software_version[0],
                )
            ),
        ]
    )
else:
    menu_items = (
        _applications[0],
        _software[0],
        _software_version[0],
        _application_types[0],
    )