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
    
    tenant = tables.Column(
        linkify=True
    )
    
    virtual_machine = tables.Column(
        linkify=True
    )
    
    cluster_group = tables.Column(
        linkify=True
    )
        
    cluster = tables.Column(
        linkify=True
    )
        
    device = tables.Column(
        linkify=True
    )
    
    software = tables.Column(
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
        fields = ['name', 'status', 'status_date', 'tenant', 'url', 'description', 'tags', 'tenant_group', 'virtual_machine', 'cluster', 'device', 'comments', 'software']
        default_columns = [ 'name', 'software', 'version', 'url', 'tenant', 'status', 'status_date' ]