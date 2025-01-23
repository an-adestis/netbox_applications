from netbox.views import generic
from adestis_netbox_applications.forms import *
from adestis_netbox_applications.models import *
from adestis_netbox_applications.filtersets import *
from adestis_netbox_applications.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _

__all__ = (
    'ApplicationView',
    'ApplicationListView',
    'ApplicationEditView',
    'ApplicationDeleteView',
    'ApplicationBulkDeleteView',
    'ApplicationBulkEditView',
    'ApplicationBulkImportView',
)

class ApplicationView(generic.ObjectView):
    queryset = Application.objects.all()


class ApplicationListView(generic.ObjectListView):
    queryset = Application.objects.all()
    table = ApplicationTable
    filterset = ApplicationFilterSet
    filterset_form = ApplicationFilterForm

class ApplicationEditView(generic.ObjectEditView):
    queryset = Application.objects.all()
    form = ApplicationForm


class ApplicationDeleteView(generic.ObjectDeleteView):
    queryset = Application.objects.all()
 

class ApplicationBulkDeleteView(generic.BulkDeleteView):
    queryset = Application.objects.all()
    table = ApplicationTable
    
    
class ApplicationBulkEditView(generic.BulkEditView):
    queryset = Application.objects.all()
    filterset = ApplicationFilterSet
    table = ApplicationTable
    form =  ApplicationBulkEditForm
    

class ApplicationBulkImportView(generic.BulkImportView):
    queryset = Application.objects.all()
    model_form = ApplicationCSVForm
    table = ApplicationTable
    

