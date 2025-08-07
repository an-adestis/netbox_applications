from netbox.views import generic
from adestis_netbox_applications.forms.application_types import *
from adestis_netbox_applications.models.application_types import *
from adestis_netbox_applications.models.application import *
from adestis_netbox_applications.filtersets.application_types import *
from adestis_netbox_applications.tables.application_types import *
from netbox.views import generic
from django.utils.translation import gettext as _
from utilities.views import GetRelatedModelsMixin, ViewTab, register_model_view
from utilities.query import count_related


__all__ = (
    'InstalledApplicationTypesView',
    'InstalledApplicationTypesListView',
    'InstalledApplicationTypesEditView',
    'InstalledApplicationTypesDeleteView',
    'InstalledApplicationTypesBulkDeleteView',
    'InstalledApplicationTypesBulkEditView',
    'InstalledApplicationTypesBulkImportView',

)


@register_model_view(InstalledApplicationTypes)
class InstalledApplicationTypesView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = InstalledApplicationTypes.objects.all()
    def get_extra_context(self, request, instance):
        return {
            'related_models': self.get_related_models(request, instance),
        }

class InstalledApplicationTypesListView(generic.ObjectListView):
    queryset = InstalledApplicationTypes.objects.annotate(
        application_count=count_related(InstalledApplication, 'application_types')
    )
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
    