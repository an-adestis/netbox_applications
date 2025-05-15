from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_applications.models import InstalledApplication
from adestis_netbox_applications.filtersets import *
import django_tables2 as tables
from dcim.models import *

class InstalledApplicationTable(NetBoxTable):
    status = ChoiceFieldColumn()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    version = columns.MarkdownColumn()
    
    url = columns.MarkdownColumn(
        linkify=True
    )
    
    status_date = columns.DateColumn()

    class Meta(NetBoxTable.Meta):
        model = InstalledApplication
        fields = ['name', 'status', 'status_date', 'tenant', 'url', 'description', 'tags', 'tenant_group', 'virtual_machine', 'cluster', 'device', 'comments', 'software']
        default_columns = [ 'name', 'tenant', 'status', 'status_date' ]
        
class DeviceInstalledApplicationListTable(NetBoxTable):
    
    parent = tables.Column(
        verbose_name=('Parent'),
        linkify=True
    )
    bridge = tables.Column(
        verbose_name=('Bridge'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Device
        fields = (
            'pk', 'id', 'name', 'enabled', 'parent', 'bridge', 'primary_mac_address', 'mtu', 'mode', 'description',
            'tags', 'vrf', 'l2vpn', 'tunnel', 'ip_addresses', 'fhrp_groups', 'untagged_vlan', 'tagged_vlans',
            'qinq_svlan', 'actions', 'installed_application',
        )
        default_columns = ('pk', 'name', 'enabled', 'primary_mac_address', 'mtu', 'mode', 'description', 'ip_addresses', 'installed_application')
        row_attrs = {
            'data-name': lambda record: record.name,
            'data-virtual': lambda record: "true",
            'data-enabled': lambda record: "true" if record.enabled else "false",
        }
             

class ClusterInstalledApplicationListTable(NetBoxTable):
    
    parent = tables.Column(
        verbose_name=('Parent'),
        linkify=True
    )
    bridge = tables.Column(
        verbose_name=('Bridge'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Device
        fields = (
            'pk', 'id', 'name', 'enabled', 'parent', 'bridge', 'primary_mac_address', 'mtu', 'mode', 'description',
            'tags', 'vrf', 'l2vpn', 'tunnel', 'ip_addresses', 'fhrp_groups', 'untagged_vlan', 'tagged_vlans',
            'qinq_svlan', 'actions',
        )
        default_columns = ('pk', 'name', 'enabled', 'primary_mac_address', 'mtu', 'mode', 'description', 'ip_addresses')
        row_attrs = {
            'data-name': lambda record: record.name,
            'data-virtual': lambda record: "true",
            'data-enabled': lambda record: "true" if record.enabled else "false",
        }  
class ClusterGroupInstalledApplicationListTable(NetBoxTable):
    
    parent = tables.Column(
        verbose_name=('Parent'),
        linkify=True
    )
    bridge = tables.Column(
        verbose_name=('Bridge'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Device
        fields = (
            'pk', 'id', 'name', 'enabled', 'parent', 'bridge', 'primary_mac_address', 'mtu', 'mode', 'description',
            'tags', 'vrf', 'l2vpn', 'tunnel', 'ip_addresses', 'fhrp_groups', 'untagged_vlan', 'tagged_vlans',
            'qinq_svlan', 'actions',
        )
        default_columns = ('pk', 'name', 'enabled', 'primary_mac_address', 'mtu', 'mode', 'description', 'ip_addresses')
        row_attrs = {
            'data-name': lambda record: record.name,
            'data-virtual': lambda record: "true",
            'data-enabled': lambda record: "true" if record.enabled else "false",
        }
class VirtualMachineInstalledApplicationListTable(NetBoxTable):
    
    parent = tables.Column(
        verbose_name=('Parent'),
        linkify=True
    )
    bridge = tables.Column(
        verbose_name=('Bridge'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Device
        fields = (
            'pk', 'id', 'name', 'enabled', 'parent', 'bridge', 'primary_mac_address', 'mtu', 'mode', 'description',
            'tags', 'vrf', 'l2vpn', 'tunnel', 'ip_addresses', 'fhrp_groups', 'untagged_vlan', 'tagged_vlans',
            'qinq_svlan', 'actions',
        )
        default_columns = ('pk', 'name', 'enabled', 'primary_mac_address', 'mtu', 'mode', 'description', 'ip_addresses')
        row_attrs = {
            'data-name': lambda record: record.name,
            'data-virtual': lambda record: "true",
            'data-enabled': lambda record: "true" if record.enabled else "false",
        }