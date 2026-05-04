from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_applications.models import InstalledApplication
from adestis_netbox_applications.filtersets import *
import django_tables2 as tables
from dcim.models import *
from dcim.tables import *
from tenancy.models import *
from tenancy.tables.contacts import ContactTable
from tenancy.forms import *
from dcim.models import *
from dcim.forms import *
from dcim.tables import *
from dcim.filtersets import *
from netbox.constants import DEFAULT_ACTION_PERMISSIONS
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
import django_tables2 as tables

from django.utils.safestring import mark_safe

class InstalledApplicationTable(NetBoxTable):
    
    status = ChoiceFieldColumn()
    
    approval_status = ChoiceFieldColumn()

    comments = columns.MarkdownColumn()
    
    approval_info = columns.MarkdownColumn()

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
    
    contact = columns.ManyToManyColumn(
        linkify_item=True
    )
    
    contact_group = tables.Column(
        linkify=True
    )
    
    software = tables.Column(
        linkify = True
    )
    
    software_version = tables.Column(
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
    
    parent_application = tables.Column(
        linkify=True
    )
    
    software_version_count= columns.LinkedCountColumn(
        viewname='plugins:adestis_netbox_applications:softwareversion_list',
        url_params={'installedapplication_id': 'pk'},
        verbose_name=('Software Version')
    )
    
    def render_name(self, value, record):
        depth = 0
        parent = record.parent_application
        while parent:
            depth += 1
            parent = parent.parent_application

        link = f'<a href="{record.get_absolute_url()}">{record.name}</a>'
        parent_pk = record.parent_application.pk if record.parent_application else ''

        return mark_safe(
            f'<span style="display:inline-block; min-width:{depth * 20}px;"></span>'
            f'<span data-pk="{record.pk}" data-parent="{parent_pk}" data-depth="{depth}" style="display:inline-flex; align-items:center;">'
            f'{link}</span>'
        )
    
    class Meta(NetBoxTable.Meta):
        model = InstalledApplication
        fields = ['name', 'application_types', 'status', 'status_date', 'software_version', 'software_version_count', 'approval_status', 'parent_application', 'tenant', 'url', 'description', 'tags', 'tenant_group', 'virtual_machine', 'cluster',  'cluster_group', 'device', 'contact', 'contact_group', 'comments', 'approval_info', 'software', 'actions']
        default_columns = [ 'name', 'application_types', 'software', 'version', 'software_version_count', 'url', 'tenant', 'contact', 'status', 'status_date', 'approval_status']

class InstalledApplicationTableTab(InstalledApplicationTable):
    
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    class Meta(InstalledApplicationTable.Meta):
        fields = ('name', 'application_types', 'status', 'status_date', 'approval_status', 'software_version', 'software_version_count', 'parent_application', 'tenant', 'url', 'description', 'tags', 'tenant_group', 'virtual_machine', 'cluster', 'cluster_group', 'device', 'contact', 'contact_group', 'comments', 'approval_info', 'software', 'actions')
        default_columns = ( 'name', 'application_types', 'software', 'version', 'software_version_count', 'url', 'tenant', 'contact', 'status', 'status_date', 'approval_status')
        
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
        
class ContactTableInstalledApplication(ContactTable):
    
    actions = columns.ActionsColumn(
        actions=('edit', ),
    )
    
    class Meta(ContactTable.Meta):
        fields = (
            'pk', 'name', 'groups', 'title', 'phone', 'email', 'address', 'link', 'description', 'comments',
            'assignment_count', 'tags', 'created', 'last_updated', 'actions'
        )
        default_columns = ('pk', 'name', 'groups', 'assignment_count', 'title', 'phone', 'email')
        
