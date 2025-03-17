from netbox.views import generic
from adestis_netbox_applications.forms.software import *
from adestis_netbox_applications.models.software import *
from adestis_netbox_applications.filtersets.software import *
from adestis_netbox_applications.tables.software import *
from netbox.views import generic
from django.utils.translation import gettext as _

__all__ = (
    'SoftwareView',
    'SoftwareListView',
    'SoftwareEditView',
    'SoftwareDeleteView',
    'SoftwareBulkDeleteView',
    'SoftwareBulkEditView',
    'SoftwareBulkImportView',
)

class SoftwareView(generic.ObjectView):
    queryset = Software.objects.all()

class SoftwareListView(generic.ObjectListView):
    queryset = Software.objects.all()
    table = SoftwareTable
    filterset = SoftwareFilterSet
    filterset_form = SoftwareFilterForm
    

class SoftwareEditView(generic.ObjectEditView):
    queryset = Software.objects.all()
    form = SoftwareForm


class SoftwareDeleteView(generic.ObjectDeleteView):
    queryset = Software.objects.all() 

class SoftwareBulkDeleteView(generic.BulkDeleteView):
    queryset = Software.objects.all()
    table = SoftwareTable
    
    
class SoftwareBulkEditView(generic.BulkEditView):
    queryset = Software.objects.all()
    filterset = SoftwareFilterSet
    table = SoftwareTable
    form =  SoftwareBulkEditForm
    

class SoftwareBulkImportView(generic.BulkImportView):
    queryset = Software.objects.all()
    model_form = SoftwareCSVForm
    table = SoftwareTable
    