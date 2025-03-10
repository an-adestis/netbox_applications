from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_applications.models import InstalledApplication
from adestis_netbox_applications.filtersets import *


class InstalledApplicationTable(NetBoxTable):
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
        model = InstalledApplication
        fields = ['name', 'status', 'tenant', 'version', 'url', 'description', 'tags', 'tenant_group', 'manufacturer', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'comments',]
        default_columns = [ 'name', 'tenant', 'version', 'status' ]
        