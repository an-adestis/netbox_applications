from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_applications.models.application_types import InstalledApplicationTypes
from adestis_netbox_applications.filtersets.application_types import *


class InstalledApplicationTypesTable(NetBoxTable):

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    comment = columns.MarkdownColumn()
    
    class Meta(NetBoxTable.Meta):
        model = InstalledApplicationTypes
        fields = ['name',  'comment', 'tags',]
        default_columns = [ 'name',]
        