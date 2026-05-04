from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_applications.models.software import Software
from adestis_netbox_applications.models.software_version import SoftwareVersion
from adestis_netbox_applications.filtersets.software import *
import django_tables2 as tables


class SoftwareVersionTable(NetBoxTable):
    
    approval_status = ChoiceFieldColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )
    
    version = columns.MarkdownColumn()

    description = columns.MarkdownColumn()
    
    approval_info = columns.MarkdownColumn()

    software = tables.Column(
        linkify=True
    )
    
    software_count = columns.LinkedCountColumn(
        viewname='plugins:adestis_netbox_applications:software_list',
        url_params={'software_version_id': 'pk'},
        verbose_name=('Software')
    )

    class Meta(NetBoxTable.Meta):
        model = SoftwareVersion
        fields = ['name', 'version', 'approval_status', 'software', 'software_count', 'description', 'tags', 'approval_info']
        default_columns = ['name', 'software_count', 'version', 'approval_status', 'approval_info']
    
