from netbox.views import generic
from adestis_netbox_applications.forms.application import *
from adestis_netbox_applications.filtersets.application import *
from adestis_netbox_applications.models.application import InstalledApplication, ClusterAssignment, DeviceAssignment, ClusterGroupAssignment, VirtualMachineAssignment
from adestis_netbox_applications.filtersets import *
from adestis_netbox_applications.tables import *
from netbox.views import generic
from django.db.models import Prefetch
from django.utils.translation import gettext as _
from tenancy.models import *
from dcim.models import *
from dcim.forms import *
from dcim.tables import *
from dcim.filtersets import *
from netbox.constants import DEFAULT_ACTION_PERMISSIONS
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
from utilities.views import GetRelatedModelsMixin, ViewTab, register_model_view
from utilities.views import ViewTab, register_model_view
from django.shortcuts import get_object_or_404
from core.models import ObjectType as ContentType
from django.contrib.contenttypes.models import ContentType

__all__ = (
    'InstalledApplicationView',
    'InstalledApplicationListView',
    'InstalledApplicationEditView',
    'InstalledApplicationDeleteView',
    'DeviceAssignmentDeleteView',
    'ClusterAssignmentDeleteView',
    'ClusterGroupAssignmentDeleteView',
    'VirtualMachineAssignmentDeleteView',
    'InstalledApplicationBulkDeleteView',
    'InstalledApplicationBulkEditView',
    'InstalledApplicationBulkImportView',
    'DeviceAffectedInstalledApplicationView',
    'ClusterAffectedInstalledApplicationView',
    'ClusterGroupAffectedInstalledApplicationView',
    'VirtualMachineAffectedInstalledApplicationView',
)

class InstalledApplicationView(generic.ObjectView):
    queryset = InstalledApplication.objects.all()
    
class InstalledApplicationListView(generic.ObjectListView):
    queryset = InstalledApplication.objects.all()
    table = InstalledApplicationTable
    filterset = InstalledApplicationFilterSet
    filterset_form = InstalledApplicationFilterForm
    

class InstalledApplicationEditView(generic.ObjectEditView):
    queryset = InstalledApplication.objects.all()
    form = InstalledApplicationForm


class InstalledApplicationDeleteView(generic.ObjectDeleteView):
    queryset = InstalledApplication.objects.all() 

class ClusterAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = ClusterAssignment.objects.all() 
    
class ClusterGroupAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = ClusterGroupAssignment.objects.all() 
    
class DeviceAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = DeviceAssignment.objects.all() 
    
class VirtualMachineAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = VirtualMachineAssignment.objects.all() 

class InstalledApplicationBulkDeleteView(generic.BulkDeleteView):
    queryset = InstalledApplication.objects.all()
    table = InstalledApplicationTable
    
    
class InstalledApplicationBulkEditView(generic.BulkEditView):
    queryset = InstalledApplication.objects.all()
    filterset = InstalledApplicationFilterSet
    table = InstalledApplicationTable
    form =  InstalledApplicationBulkEditForm
    

class InstalledApplicationBulkImportView(generic.BulkImportView):
    queryset = InstalledApplication.objects.all()
    model_form = InstalledApplicationCSVForm
    table = InstalledApplicationTable
    
@register_model_view(InstalledApplication, name='devices')
class DeviceAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= Device
    table = DeviceTable
    template_name = "adestis_netbox_applications/device.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_device': {'change'},
    }

    tab = ViewTab(
        label=_('Devices'),
        badge=lambda obj: obj.device.count(),
        weight=600
    )

    def get_children(self, request, parent):
        return Device.objects.restrict(request.user, 'view').filter(installedapplication=parent)

@register_model_view(Device, name='applications')
class DeviceAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = Device.objects.all()
    child_model= InstalledApplication
    table = InstalledApplicationTable
    template_name = "adestis_netbox_applications/assign_device.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_device': {'change'},
    }

    tab = ViewTab(
        label=_('Applications'),
        badge=lambda obj: obj.installedapplication.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return InstalledApplication.objects.restrict(request.user, 'view').filter(device=parent)
 

@register_model_view(InstalledApplication, name='clusters')
class ClusterAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= Cluster
    table = ClusterTable
    template_name = "adestis_netbox_applications/cluster.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_device': {'change'},
    }

    tab = ViewTab(
        label=_('Clusters'),
        badge=lambda obj: obj.cluster.count(),
        weight=600
    )

    def get_children(self, request, parent):
        return Cluster.objects.restrict(request.user, 'view').filter(installedapplication=parent)
 
@register_model_view(Cluster, name='applications')
class ClusterAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = Cluster.objects.all()
    child_model= InstalledApplication
    table = InstalledApplicationTable
    template_name = "adestis_netbox_applications/assign_cluster.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_device': {'change'},
    }

    tab = ViewTab(
        label=_('Applications'),
        badge=lambda obj: obj.installedapplication.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return InstalledApplication.objects.restrict(request.user, 'view').filter(cluster=parent)
    
    
@register_model_view(InstalledApplication, name='cluster groups')
class ClusterGroupAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= ClusterGroup
    table = ClusterGroupTable
    template_name = "adestis_netbox_applications/cluster_group.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_device': {'change'},
    }

    tab = ViewTab(
        label=_('Cluster Groups'),
        badge=lambda obj: obj.cluster_group.count(),
        weight=600
    )

    def get_children(self, request, parent):
        return ClusterGroup.objects.restrict(request.user, 'view').filter(installedapplication=parent)

@register_model_view(ClusterGroup, name='applications')
class ClusterGroupAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = VirtualMachine.objects.all()
    child_model= InstalledApplication
    table = InstalledApplicationTable
    template_name = "adestis_netbox_applications/assign_cluster_group.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_device': {'change'},
    }

    tab = ViewTab(
        label=_('Applications'),
        badge=lambda obj: obj.installedapplication.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return InstalledApplication.objects.restrict(request.user, 'view').filter(cluster_group=parent)


@register_model_view(InstalledApplication, name='virtual machines')
class VirtualMachineAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= VirtualMachine
    table = VirtualMachineTable
    template_name = "adestis_netbox_applications/assign_virtual_machine.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_device': {'change'},
    }

    tab = ViewTab(
        label=_('Virtual Machines'),
        badge=lambda obj: obj.virtual_machine.count(),
        weight=600
    )

    def get_children(self, request, parent):
        return VirtualMachine.objects.restrict(request.user, 'view').filter(installedapplication=parent)
  
@register_model_view(VirtualMachine, name='applications')
class VirtualMachineAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = VirtualMachine.objects.all()
    child_model= InstalledApplication
    table = InstalledApplicationTable
    template_name = "adestis_netbox_applications/virtual_machine.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_device': {'change'},
    }

    tab = ViewTab(
        label=_('Applications'),
        badge=lambda obj: obj.installedapplication.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return InstalledApplication.objects.restrict(request.user, 'view').filter(virtual_machine=parent)
