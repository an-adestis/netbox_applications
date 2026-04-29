from netbox.views import generic
from adestis_netbox_applications.forms.software_version import *
from adestis_netbox_applications.models.software_version import *
from adestis_netbox_applications.filtersets.software_version import *
from adestis_netbox_applications.tables.software_version import *
from netbox.views import generic
from django.utils.translation import gettext as _
from utilities.views import GetRelatedModelsMixin, ViewTab, register_model_view

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db import transaction
from django.contrib import messages

__all__ = (
    'SoftwareVersionView',
    'SoftwareVersionListView',
    'SoftwareVersionEditView',
    'SoftwareVersionDeleteView',
    'SoftwareVersionBulkDeleteView',
    'SoftwareVersionBulkEditView',
    'SoftwareVersionBulkImportView',
)

class SoftwareVersionView(generic.ObjectView):
    queryset = SoftwareVersion.objects.all()

class SoftwareVersionListView(generic.ObjectListView):
    queryset = SoftwareVersion.objects.all()
    table = SoftwareVersionTable
    filterset = SoftwareVersionFilterSet
    filterset_form = SoftwareVersionFilterForm
    

class SoftwareVersionEditView(generic.ObjectEditView):
    queryset = SoftwareVersion.objects.all()
    form = SoftwareVersionForm


class SoftwareVersionDeleteView(generic.ObjectDeleteView):
    queryset = SoftwareVersion.objects.all() 

class SoftwareVersionBulkDeleteView(generic.BulkDeleteView):
    queryset = SoftwareVersion.objects.all()
    table = SoftwareVersionTable
    
    
class SoftwareVersionBulkEditView(generic.BulkEditView):
    queryset = SoftwareVersion.objects.all()
    filterset = SoftwareVersionFilterSet
    table = SoftwareVersionTable
    form =  SoftwareVersionBulkEditForm
    

class SoftwareVersionBulkImportView(generic.BulkImportView):
    queryset = SoftwareVersion.objects.all()
    model_form = SoftwareVersionCSVForm
    table = SoftwareVersionTable