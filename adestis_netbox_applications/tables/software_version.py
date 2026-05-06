from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_applications.models.software import Software
from adestis_netbox_applications.models.software_version import SoftwareVersion
from adestis_netbox_applications.filtersets.software import *
import django_tables2 as tables

from django.utils.safestring import mark_safe

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
    
    installed_applications = tables.Column(
        empty_values=(),
        verbose_name='Applications',
        orderable=False,
    )

    def render_installed_applications(self, value, record):
        applications = record.applications_software_version.all()
        if not applications:
            return '-'
        links = ', '.join(
            f'<a href="{v.get_absolute_url()}">{v.name}</a>' for v in applications
        )
        return mark_safe(links)

    class Meta(NetBoxTable.Meta):
        model = SoftwareVersion
        fields = ['name', 'version', 'approval_status', 'software', 'installed_applications', 'description', 'tags', 'approval_info']
        default_columns = ['name', 'version', 'software', 'installed_applications', 'approval_status', 'approval_info']