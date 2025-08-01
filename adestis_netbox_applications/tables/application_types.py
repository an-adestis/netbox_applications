from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_applications.models.application_types import InstalledApplicationTypes
from adestis_netbox_applications.filtersets.application_types import *
import django_tables2 as tables

class InstalledApplicationTypesTable(NetBoxTable):

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    
    installedapplication = tables.Column(
        linkify=True
    )
    
    application_count = columns.LinkedCountColumn(
        viewname='plugins:adestis_netbox_applications:installedapplication_list',
        url_params={'installedapplicationtypes_id': 'pk'},
        verbose_name=('Application')
    )
    
    class Meta(NetBoxTable.Meta):
        model = InstalledApplicationTypes
        fields = ['name', 'slug', 'tags', 'installedapplication', 'application_count']
        default_columns = [ 'name', 'application_count']
        