from netbox.views import generic
from adestis_netbox_applications.forms import *
from adestis_netbox_applications.models import InstalledApplication, DeviceAssignment, ClusterAssignment, ClusterGroupAssignment, VirtualMachineAssignment
from adestis_netbox_applications.filtersets import *
from adestis_netbox_applications.tables import *
from netbox.views import generic
from django.db.models import Prefetch
from django.utils.translation import gettext as _
from tenancy.models import *
from dcim.models import *
from dcim.forms import *
from dcim.filtersets import *
from dcim.filterset_fo import *
from netbox.constants import DEFAULT_ACTION_PERMISSIONS
from virtualization.models import *
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
    'InstalledApplicationBulkDeleteView',
    'InstalledApplicationBulkEditView',
    'InstalledApplicationBulkImportView',
    'DeviceAffectedInstalledApplicationView',
    'DeviceAssignmentEditView',
    'DeviceAssignmentBulkDeleteView',
    'ClusterAffectedInstalledApplicationView',
    'ClusterAssignmentEditView',
    'ClusterAssignmentBulkDeleteView',
    'ClusterGroupAffectedInstalledApplicationView',
    'ClusterGroupAssignmentEditView',
    'ClusterGroupAssignmentBulkDeleteView',
    'VirtualMachineAffectedInstalledApplicationView',
    'VirtualMachineAssignmentEditView',
    'VirtualMachineAssignmentBulkDeleteView',
)

class InstalledApplicationView(generic.ObjectView):
    queryset = InstalledApplication.objects.all()
    
#     def get_extra_context(self, request, instance):
#         # match2 = InstalledApplication.objects.get(pk = request.pk)
#         # matcg3 = match2.device.all()
#         return {
#             'related_models': self.get_related_models(
#                 request,
#                 instance,
#                 extra=(
#                     # (Device.objects.restrict(request.user, 'view').filter(id__in=[instance]), 'installedapplication_id'),
#                     # (VirtualMachine.objects.restrict(request.user, 'view').filter(installedapplication__in=[instance]), 'installedapplication_id')
#                 ),
#             ),
#         }
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
    child_model= InstalledApplication
    table = DeviceInstalledApplicationListTable
    template_name = "adestis_netbox_applications/application_device.html"
    tab = ViewTab(label='Devices', badge=lambda obj: DeviceAssignment.objects.filter(installed_application=obj).count(), hide_if_empty=True)
    
    def get_children(self, request, parent):  
            children = DeviceAssignment.objects.filter(installed_application=parent)
            return children

class DeviceAssignmentEditView(generic.ObjectChildrenView):
    queryset = Device.objects.all()
    form = DeviceForm
    template_name = "dcim/dcim/device.html"
    table = tables.VirtualMachineVMInterfaceTable
    filterset = filtersets.DeviceFilterSet
    filterset_form = forms.DeviceFilterForm
    actions = {
        **DEFAULT_ACTION_PERMISSIONS,
        'bulk_rename': {'change'},
    }
    tab = ViewTab(
        label=_('Interfaces'),
        badge=lambda obj: obj.interface_count,
        permission='dcim.view_device',
        weight=500
    )

    def get_children(self, request, parent):
        return parent.interfaces.restrict(request.user, 'view').prefetch_related(
            Prefetch('ip_addresses', queryset=IPAddress.objects.restrict(request.user)),
            'tags',
        )
        
class DeviceAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = DeviceAssignment.objects.all()
    table = DeviceExploitListTable
    
@register_model_view(InstalledApplication, name='clusters')
class ClusterAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= InstalledApplication
    table = ClusterInstalledApplicationListTable
    template_name = "adestis_netbox_applications/application_cluster.html"
    tab = ViewTab(label='Clusters', badge=lambda obj: ClusterAssignment.objects.filter(installed_application=obj).count(), hide_if_empty=True)
    
    def get_children(self, request, parent):  
            children = ClusterAssignment.objects.filter(installed_application=parent)
            return children

class ClusterAssignmentEditView(generic.ObjectEditView):
    queryset = ClusterAssignment.objects.all()
    form = ClusterAssignmentForm
    template_name = "adestis_netbox_applications/generic_cluster_assignment_edit.html"

    def alter_object(self, instance, request, args, kwargs):

        if not instance.pk:
            # Assign the object based on URL kwargs
            content_type = get_object_or_404(
                ContentType, pk=request.GET.get("application_type")
            )
            instance.object = get_object_or_404(
                content_type.model_class(), pk=request.GET.get("application_id")
            )
        else:
            instance.object = instance.application
        return instance
    
    def get_extra_addanother_params(self, request):
        return {
            "application_type": request.GET.get("application_type"),
            "application_id": request.GET.get("application_id"),
        }
        
class ClusterAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = ClusterAssignment.objects.all()
    table = ClusterExploitListTable
    
    
    
@register_model_view(InstalledApplication, name='cluster groups')
class ClusterGroupAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= InstalledApplication
    table = ClusterGroupInstalledApplicationListTable
    template_name = "adestis_netbox_applications/application_cluster_group.html"
    tab = ViewTab(label='Cluster Group', badge=lambda obj: ClusterGroupAssignment.objects.filter(installed_application=obj).count(), hide_if_empty=True)
    
    def get_children(self, request, parent):  
            children = ClusterGroupAssignment.objects.filter(installed_application=parent)
            return children

class ClusterGroupAssignmentEditView(generic.ObjectEditView):
    queryset = ClusterGroupAssignment.objects.all()
    form = ClusterGroupAssignmentForm
    template_name = "adestis_netbox_applications/generic_cluster_group_assignment_edit.html"

    def alter_object(self, instance, request, args, kwargs):

        if not instance.pk:
            # Assign the object based on URL kwargs
            content_type = get_object_or_404(
                ContentType, pk=request.GET.get("application_type")
            )
            instance.object = get_object_or_404(
                content_type.model_class(), pk=request.GET.get("application_id")
            )
        else:
            instance.object = instance.application 
        return instance
    
    def get_extra_addanother_params(self, request):
        return {
            "application_type": request.GET.get("application_type"),
            "application_id": request.GET.get("application_id"),
        }
        
class ClusterGroupAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = ClusterGroupAssignment.objects.all()
    table = ClusterGroupExploitListTable
    
    
@register_model_view(InstalledApplication, name='virtual machines')
class VirtualMachineAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= InstalledApplication
    table = VirtualMachineInstalledApplicationListTable
    template_name = "adestis_netbox_applications/application_virtual_machine.html"
    tab = ViewTab(label='Virtual Machines', badge=lambda obj: VirtualMachineAssignment.objects.filter(installed_application=obj).count(), hide_if_empty=True)
    
    def get_children(self, request, parent):  
            children = VirtualMachineAssignment.objects.filter(installed_application=parent)
            return children

class VirtualMachineAssignmentEditView(generic.ObjectEditView):
    queryset = VirtualMachineAssignment.objects.all()
    form = VirtualMachineAssignmentForm
    template_name = "adestis_netbox_applications/generic_virtual_machine_assignment_edit.html"

    def alter_object(self, instance, request, args, kwargs):

        if not instance.pk:
            # Assign the object based on URL kwargs
            content_type = get_object_or_404(
                ContentType, pk=request.GET.get("application_type")
            )
            instance.object = get_object_or_404(
                content_type.model_class(), pk=request.GET.get("application_id")
            )
        else:
            instance.object = instance.application
        return instance
    
    def get_extra_addanother_params(self, request):
        return {
            "application_type": request.GET.get("application_type"),
            "application_id": request.GET.get("application_id"),
        }
        
class VirtualMachineAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = VirtualMachineAssignment.objects.all()
    table = VirtualMachineExploitListTable