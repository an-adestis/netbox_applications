from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_applications.models import InstalledApplication
from adestis_netbox_applications.filtersets import *
import django_tables2 as tables
from dcim.models import *
from dcim.tables import *
from tenancy.models import *
from dcim.models import *
from dcim.forms import *
from dcim.tables import *
from dcim.filtersets import *
from netbox.constants import DEFAULT_ACTION_PERMISSIONS
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *

class InstalledApplicationTable(NetBoxTable):
    
    status = ChoiceFieldColumn()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )
    
    tenant = tables.Column(
        linkify=True
    )
    
    virtual_machine = columns.ManyToManyColumn(
        linkify_item=True
    )
    
    cluster_group = columns.ManyToManyColumn(
        linkify_item=True
    )
        
    cluster = columns.ManyToManyColumn(
        linkify_item=True
    )
        
    device = columns.ManyToManyColumn(
        linkify_item=True
    )
    
    software = tables.Column(
        linkify = True
    )
    
    application_types = tables.Column(
        linkify = True
    )

    description = columns.MarkdownColumn()
    
    version = columns.MarkdownColumn()
    
    url = columns.MarkdownColumn(
        linkify=True
    )
    
    status_date = columns.DateColumn()

    class Meta(NetBoxTable.Meta):
        model = InstalledApplication
        fields = ['name', 'application_types', 'status', 'status_date', 'tenant', 'url', 'description', 'tags', 'tenant_group', 'virtual_machine', 'cluster', 'cluster_group', 'device', 'comments', 'software', 'actions']
        default_columns = [ 'name', 'application_types', 'software', 'version', 'url', 'tenant', 'status', 'status_date' ]

class InstalledApplicationTableTab(InstalledApplicationTable):
    
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    class Meta(InstalledApplicationTable.Meta):
        fields = ('name', 'application_types', 'status', 'status_date', 'tenant', 'url', 'description', 'tags', 'tenant_group', 'virtual_machine', 'cluster', 'cluster_group', 'device', 'comments', 'software', 'actions')
        default_columns = ( 'name', 'application_types', 'software', 'version', 'url', 'tenant', 'status', 'status_date' )
        
class DeviceTableApplication(DeviceTable):
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    class Meta(DeviceTable.Meta):  
        fields = (
            'pk', 'id', 'name', 'status', 'tenant', 'tenant_group', 'role', 'manufacturer', 'device_type',
            'serial', 'asset_tag', 'region', 'site_group', 'site', 'location', 'rack', 'parent_device',
            'device_bay_position', 'position', 'face', 'latitude', 'longitude', 'airflow', 'primary_ip', 'primary_ip4',
            'primary_ip6', 'oob_ip', 'cluster', 'virtual_chassis', 'vc_position', 'vc_priority', 'description',
            'config_template', 'comments', 'contacts', 'tags', 'created', 'last_updated', 'actions',
        )
        default_columns = (
            'pk', 'name', 'status', 'tenant', 'site', 'location', 'rack', 'role', 'manufacturer', 'device_type',
            'primary_ip',
        ) 
        
class ClusterTableApplication(ClusterGroupTable):
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    class Meta(ClusterTable.Meta):
        fields = [
            'pk', 'id', 'name', 'type', 'group', 'status', 'tenant', 'tenant_group', 'site', 'description', 'comments',
            'device_count', 'vm_count', 'contacts', 'tags', 'created', 'last_updated', 'actions',
        ]
        default_columns = ['pk', 'name', 'type', 'group', 'status', 'tenant', 'site', 'device_count', 'vm_count']       

class ClusterGroupTableApplication(ClusterGroupTable):
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    class Meta(ClusterGroupTable.Meta):
        fields = [
            'pk', 'id', 'name', 'slug', 'cluster_count', 'description', 'contacts', 'tags', 'created', 'last_updated',
            'actions',
        ]
        default_columns = ['pk', 'name', 'cluster_count', 'description']
        
        
        
class VirtualMachineTableApplication(VirtualMachineTable):
    
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    class Meta(VirtualMachineTable.Meta):
        fields = [
            'pk', 'id', 'name', 'status', 'site', 'cluster', 'device', 'role', 'tenant', 'tenant_group', 'vcpus',
            'memory', 'disk', 'primary_ip4', 'primary_ip6', 'primary_ip', 'description', 'comments', 'config_template',
            'serial', 'contacts', 'tags', 'created', 'last_updated', 'actions',
        ]
        default_columns = [
            'pk', 'name', 'status', 'site', 'cluster', 'role', 'tenant', 'vcpus', 'memory', 'disk', 'primary_ip',
        ]
        
