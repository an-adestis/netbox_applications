from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_applications.models import InstalledApplication, DeviceAssignment, ClusterAssignment, ClusterGroupAssignment, VirtualMachineAssignment
from adestis_netbox_applications.filtersets import *
import django_tables2 as tables

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
    
    status_date = columns.DateColumn()

    class Meta(NetBoxTable.Meta):
        model = InstalledApplication
        fields = ['name', 'status', 'status_date', 'tenant', 'url', 'description', 'tags', 'tenant_group', 'virtual_machine', 'cluster', 'device', 'comments', 'software']
        default_columns = [ 'name', 'tenant', 'status', 'status_date' ]
        
class DeviceInstalledApplicationListTable(NetBoxTable):
    
    device = tables.Column(verbose_name='Device', linkify = True)
    class Meta(NetBoxTable.Meta):
        model = DeviceAssignment
        fields = ['device']
        
class DeviceExploitListTable(NetBoxTable):

    device = tables.Column(linkify=True)

    application = tables.Column(verbose_name="Application")

    class Meta(NetBoxTable.Meta):
        model = DeviceAssignment
        fields = ["device", "application"]
        

class ClusterInstalledApplicationListTable(NetBoxTable):
    
    cluster = tables.Column(verbose_name='Cluster', linkify = True)
    class Meta(NetBoxTable.Meta):
        model = ClusterAssignment
        fields = ['cluster']
        
class ClusterExploitListTable(NetBoxTable):

    cluster = tables.Column(linkify=True)

    application = tables.Column(verbose_name="Application")

    class Meta(NetBoxTable.Meta):
        model = ClusterAssignment
        fields = ["cluster", "application"]
        
        
class ClusterGroupInstalledApplicationListTable(NetBoxTable):
    
    cluster_group = tables.Column(verbose_name='Cluster Group', linkify = True)
    class Meta(NetBoxTable.Meta):
        model = ClusterGroupAssignment
        fields = ['cluster group']
        
class ClusterGroupExploitListTable(NetBoxTable):

    cluster_group = tables.Column(linkify=True)

    application = tables.Column(verbose_name="Application")

    class Meta(NetBoxTable.Meta):
        model = ClusterGroupAssignment
        fields = ["cluster_group", "application"]
        
        
class VirtualMachineInstalledApplicationListTable(NetBoxTable):
    
    virtual_machine = tables.Column(verbose_name='virtual Machine', linkify = True)
    class Meta(NetBoxTable.Meta):
        model = VirtualMachineAssignment
        fields = ['virtual_machine']
        
class VirtualMachineExploitListTable(NetBoxTable):

    virtual_machine = tables.Column(linkify=True)

    application = tables.Column(verbose_name="Application")

    class Meta(NetBoxTable.Meta):
        model = VirtualMachineAssignment
        fields = ["virtual_machine", "application"]