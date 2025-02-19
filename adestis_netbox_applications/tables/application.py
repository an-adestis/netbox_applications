from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_applications.models import *
from adestis_netbox_applications.filtersets import *


class ApplicationTable(NetBoxTable):
    status = ChoiceFieldColumn()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    url = columns.MarkdownColumn(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Application
        fields = ['name', 'status', 'tenant', 'version', 'url', 'description', 'tags', 'tenant_groups', 'manufacturer', 'cluster', 'cluster_group', 'virtual_machines', 'device', 'comments',]
        default_columns = [ 'name', 'tenant', 'version', 'status' ]
        