from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_applications.models import *


class ApplicationTable(NetBoxTable):
    status = ChoiceFieldColumn()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()


    class Meta(NetBoxTable.Meta):
        model = Application
        fields = ['pk', 'id', 'status', 'comments', 'actions', 'tags', 'created', 'last_updated']
        default_columns = ['pk', 'id', 'status', 'comments', 'actions', 'tags', 'created', 'last_updated']
