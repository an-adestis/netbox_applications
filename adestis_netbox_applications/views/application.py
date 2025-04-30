from netbox.views import generic
from adestis_netbox_applications.forms import *
from adestis_netbox_applications.models import InstalledApplication
from adestis_netbox_applications.filtersets import *
from adestis_netbox_applications.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _
from tenancy.models import *
from dcim.models import *
from virtualization.models import *
from utilities.views import GetRelatedModelsMixin, ViewTab, register_model_view
from utilities.views import ViewTab, register_model_view

__all__ = (
    'InstalledapplicationView'
    'InstalledApplicationListView',
    'InstalledApplicationEditView',
    'InstalledApplicationDeleteView',
    'InstalledApplicationBulkDeleteView',
    'InstalledApplicationBulkEditView',
    'InstalledApplicationBulkImportView',
    'DeviceAffectedInstalledApplicationView',
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
    template_name = "templates/adestis_netbox_applications/application_device.html"
    tab = ViewTab(label='Devices', badge=lambda obj: InstalledApplication.objects.filter(device=obj).count(), hide_if_empty=True)