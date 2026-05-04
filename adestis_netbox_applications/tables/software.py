from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_applications.models.software import Software
from adestis_netbox_applications.filtersets.software import *
import django_tables2 as tables
from tenancy.models import *
from tenancy.tables.contacts import ContactTable

class SoftwareTable(NetBoxTable):
    
    status = ChoiceFieldColumn()
    
    approval_status = ChoiceFieldColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    approval_info = columns.MarkdownColumn()
    
    url = columns.MarkdownColumn(
        linkify=True
    )
    
    manufacturer = tables.Column(
        linkify=True
    )
    
    contact = columns.ManyToManyColumn(
        linkify_item=True
    )
    
    contact_group = tables.Column(
        linkify=True
    )
    
    parent_software = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Software
        fields = ['name', 'status', 'parent_software', 'approval_status', 'url', 'description', 'tags', 'manufacturer', 'contact', 'contact_group', 'approval_info']
        default_columns = [ 'name', 'status', 'parent_software', 'approval_status', 'approval_info', 'manufacturer', 'contact']
        
        
class ContactTableSoftware(ContactTable):
    
    actions = columns.ActionsColumn(
        actions=('edit', ),
    )
    
    class Meta(ContactTable.Meta):
        fields = (
            'pk', 'name', 'groups', 'title', 'phone', 'email', 'address', 'link', 'description', 'comments',
            'assignment_count', 'tags', 'created', 'last_updated', 'actions'
        )
        default_columns = ('pk', 'name', 'groups', 'assignment_count', 'title', 'phone', 'email')
        
