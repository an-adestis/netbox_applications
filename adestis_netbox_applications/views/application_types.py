from netbox.views import generic
from adestis_netbox_applications.forms.application_types import *
from adestis_netbox_applications.models.application_types import *
from adestis_netbox_applications.filtersets.application_types import *
from adestis_netbox_applications.tables.application_types import *
from netbox.views import generic
from django.utils.translation import gettext as _

__all__ = (
    'InstalledApplicationTypesView',
    'InstalledApplicationTypesListView',
    'InstalledApplicationTypesEditView',
    'InstalledApplicationTypesDeleteView',
    'InstalledApplicationTypesBulkDeleteView',
    'InstalledApplicationTypesBulkEditView',
    'InstalledApplicationTypesBulkImportView',
)

class InstalledApplicationTypesView(generic.ObjectView):
    queryset = InstalledApplicationTypes.objects.all()

class InstalledApplicationTypesListView(generic.ObjectListView):
    queryset = InstalledApplicationTypes.objects.all()
    table = InstalledApplicationTypesTable
    filterset = InstalledApplicationTypesFilterSet
    filterset_form = InstalledApplicationTypesFilterForm
    

class InstalledApplicationTypesEditView(generic.ObjectEditView):
    queryset = InstalledApplicationTypes.objects.all()
    form = InstalledApplicationTypesForm


class InstalledApplicationTypesDeleteView(generic.ObjectDeleteView):
    queryset = InstalledApplicationTypes.objects.all() 

class InstalledApplicationTypesBulkDeleteView(generic.BulkDeleteView):
    queryset = InstalledApplicationTypes.objects.all()
    table = InstalledApplicationTypesTable
    
    
class InstalledApplicationTypesBulkEditView(generic.BulkEditView):
    queryset = InstalledApplicationTypes.objects.all()
    filterset = InstalledApplicationTypesFilterSet
    table = InstalledApplicationTypesTable
    form =  InstalledApplicationTypesBulkEditForm
    

class InstalledApplicationTypesBulkImportView(generic.BulkImportView):
    queryset = InstalledApplicationTypes.objects.all()
    model_form = InstalledApplicationTypesCSVForm
    table = InstalledApplicationTypesTable
    