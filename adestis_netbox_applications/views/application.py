from netbox.views import generic
from adestis_netbox_applications.forms import *
from adestis_netbox_applications.models import *
from adestis_netbox_applications.filtersets import *
from adestis_netbox_applications.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _

__all__ = (
    'InstalledApplicationView',
    'InstalledApplicationListView',
    'InstalledApplicationEditView',
    'InstalledApplicationDeleteView',
    'InstalledApplicationBulkDeleteView',
    'InstalledApplicationBulkEditView',
    'InstalledApplicationBulkImportView',
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
    