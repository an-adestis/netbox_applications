from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_applications.models.application import Application, ApplicationStatusChoices
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    TagFilterField,
    CSVModelChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from tenancy.models import Tenant, TenantGroup
from dcim.models import *
from virtualization.models import *

__all__ = (
    'ApplicationForm',
    'ApplicationFilterForm',
    'ApplicationBulkEditForm',
    'ApplicationCSVForm',
)

class ApplicationForm(NetBoxModelForm):

    fieldsets = (
        FieldSet('name', 'description', 'url', 'tags', 'status', 'version', name=_('Application')),
        FieldSet('tenant_groups', 'tenant',  name=_('Tenant')), 
        FieldSet('manufacturer', 'cluster', 'cluster_group', 'virtual_machines', name=_('Virtualization')),   
        FieldSet('device', name=_('Device'))
    )

    class Meta:
        model = Application
        fields = ['name', 'description', 'url', 'tags', 'status', 'tenant', 'tenant_groups', 'manufacturer', 'cluster', 'cluster_group', 'virtual_machines', 'device', 'comments', 'version']
        
        help_texts = {
            'status': "Example text",
        }

class ApplicationBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Application.objects.all(),
        widget=forms.MultipleHiddenInput, 
    )
    
    name = forms.CharField(
        required=False,
        max_length = 150,
        label=_("Name"),
    )
    
    comments = forms.CharField(
        max_length=150,
        required=False,
        label=_("Comment")
    )
    
    url = forms.URLField(
        max_length=300,
        required=False,
        label=_("URL")
    )
    
    version = forms.CharField(
        max_length=200,
        required=False,
        label=_("Version")
    )

    status = forms.ChoiceField(
        required=False,
        choices=ApplicationStatusChoices,
    )
    
    description = forms.CharField(
        max_length=500,
        required=False,
        label=_("Description"),
    )
    
    virtual_machines = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required = False,
        label = ("Virtual Machines")
    )
    
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required = False,
        label =_("Device")
    )
    
    tenant_group = DynamicModelChoiceField(
        queryset=TenantGroup.objects.all(),
        required = False,
        label=_("Tenant Group"),
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required = False,
        label=_("Tenant"),
    )
    
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required = False,
        label=_("Manufacturer")
    )
    
    cluster_group = DynamicModelChoiceField(
        queryset=ClusterGroup.objects.all(),
        required = False,
        label=_("Cluster Group")
    )
    
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        required = False,
        label=_("Cluster")
    )
    
    model = Application

    fieldsets = (
        FieldSet('name', 'description', 'url', 'tags', 'status', 'version', 'comments', name=_('Application')),
        FieldSet('tenant_group', 'tenant', name=_('Tenant')),
        FieldSet('manufacturer', 'cluster', 'cluster_group', 'virtual_machines', name=_('Virtualization')),
        FieldSet('device', name=_('Device'))
    )

    nullable_fields = [
         'add_tags', 'remove_tags', 'description', ''
    ]
    
class ApplicationFilterForm(NetBoxModelFilterSetForm):
    
    model = Application

    fieldsets = (
        FieldSet('q', 'index', 'tag'),
        FieldSet('status'),
    )

    index = forms.IntegerField(
        required=False
    )

    status = forms.MultipleChoiceField(
        choices=ApplicationStatusChoices,
        required=False,
        label=_('Status')
    )

    tag = TagFilterField(model)


class ApplicationCSVForm(NetBoxModelImportForm):

    status = CSVChoiceField(
        choices=ApplicationStatusChoices,
        help_text=_('Status'),
        required=True,
    )
    
    tenant_groups = CSVModelChoiceField(
        label=_('Tenant Group'),
        queryset=TenantGroup.objects.all(),
        required=False,
        to_field_name='name',
        help_text=('Assigned tenant group')
    )
    
    tenant = CSVModelChoiceField(
        label=_('Tenant'),
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned tenant')
    )
    
    manufacturer = CSVModelChoiceField(
        label=_("Manufacturer"),
        queryset=Manufacturer.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned manufacturer')
    )
    
    cluster_group = CSVModelChoiceField(
        label=_('Cluster Group'),
        queryset=ClusterGroup.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned cluster group')
    )
    
    cluster = CSVModelChoiceField(
        label=_('Cluster'),
        queryset=Cluster.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned cluster')
    )
    
    virtual_machines = CSVModelChoiceField(
        label=_('Virtual Machine'),
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned virtual machine')
    )
    
    device = CSVModelChoiceField(
        label=_('Device'),
        queryset=Device.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned device')
    )

    class Meta:
        model = Application
        fields = ['name' ,'status',  'url', 'tenant', 'tenant_groups', 'manufacturer', 'cluster', 'cluster_group', 'virtual_machines', 'device', 'description',  'tags', 'comments', 'version']
        default_return_url = 'plugins:adestis_netbox_applications:Application_list'


    