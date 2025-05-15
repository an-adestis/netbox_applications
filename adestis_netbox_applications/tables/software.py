from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_applications.models.software import Software
from adestis_netbox_applications.filtersets.software import *


class SoftwareTable(NetBoxTable):
    status = ChoiceFieldColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    url = columns.MarkdownColumn(
        linkify=True
    )
    

    class Meta(NetBoxTable.Meta):
        model = Software
        fields = ['name', 'status', 'url', 'description', 'tags', 'manufacturer',]
        default_columns = [ 'name', 'status' ]
        