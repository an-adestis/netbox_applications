from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_applications.models import *
from adestis_netbox_applications.models.software import *
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    TagFilterField,
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from utilities.forms.widgets import DatePicker
from tenancy.models import Tenant, TenantGroup
from dcim.models import *
from virtualization.models import *
from adestis_netbox_applications.models.software import *

__all__ = (
    'InstalledApplicationForm',
    'InstalledApplicationFilterForm',
    'InstalledApplicationBulkEditForm',
    'InstalledApplicationCSVForm',
)

class InstalledApplicationForm(NetBoxModelForm):

    fieldsets = (
        FieldSet('name', 'description', 'version', 'software', 'url', 'tags', 'status', 'status_date',  name=_('Application')),
        FieldSet('tenant_group', 'tenant',  name=_('Tenant')), 
        FieldSet('virtual_machine', 'cluster_group', 'cluster', name=_('Virtualization')),   
        FieldSet('device', name=_('Device'))
    )

    class Meta:
        model = InstalledApplication
        fields = ['name', 'description', 'url', 'tags', 'status', 'status_date', 'tenant', 'virtual_machine', 'device', 'cluster_group', 'cluster', 'tenant_group', 'comments', 'software', 'version']
        
        help_texts = {
            'status': "Example text",
        }
        
        widgets = {
            'status_date': DatePicker(),
        }
        
class InstalledApplicationBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=InstalledApplication.objects.all(),
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
    
    status = forms.ChoiceField(
        required=False,
        choices=InstalledApplicationStatusChoices,
    )
    
    status_date = forms.DateField(
        required=False,
        widget=DatePicker
    )
    
    description = forms.CharField(
        max_length=500,
        required=False,
        label=_("Description"),
    )
    
    version = forms.CharField(
        max_length=200,
        required=False,
        label=_("Version")
    )
    
    virtual_machine = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required = False,
        label = ("Virtual Machines"),
        null_option='None'
    )

    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required = False,
        label =_("Devices"),
        null_option='None'
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
    
    software = DynamicModelChoiceField(
        queryset=Software.objects.all(),
        required= False,
        label=_('Software'),
    )
    
    cluster_group = DynamicModelChoiceField(
        queryset=ClusterGroup.objects.all(),
        required = False,
        label=_("Cluster Groups")
    )
    
    cluster = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required = False,
        label=_("Clusters"),
        null_option='None'
    )
    
    model = InstalledApplication

    fieldsets = (
        FieldSet('name', 'description', 'version', 'software', 'url', 'tags', 'status', 'status_date', 'comments', name=_('Application')),
        FieldSet('tenant_group', 'tenant', name=_('Tenant')),
        FieldSet('virtual_machine', 'cluster', name=_('Virtualization')),
        FieldSet('device', name=_('Device'))
    )

    nullable_fields = [
         'add_tags', 'remove_tags', 'description', ''
    ]
    
class InstalledApplicationFilterForm(NetBoxModelFilterSetForm):
    
    model = InstalledApplication

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'url', 'tag', 'version', 'software_id', 'status', 'status_date', name=_('Application')),
        FieldSet('tenant_group_id', 'tenant_id', name=_('Tenant')),
        FieldSet('cluster_id', 'virtual_machine_id', name=_('Virtualization')),
        FieldSet('device_id', name=_('Device'))
    )

    index = forms.IntegerField(
        required=False
    )

    status = forms.MultipleChoiceField(
        choices=InstalledApplicationStatusChoices,
        required=False,
        label=_('Status')
    )
    
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'cluster_id': '$cluster_id',
        },
        label=_('Devices')
    )
    
    virtual_machine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'cluster_id': '$cluster_id',
            'device_id': '$device_id',
        },
        label=_('Virtual Machines')
    )
    
    cluster_group_id = DynamicModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=False,
        null_option='None',
        label=_('Cluster Groups')
    )

    cluster_id = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        null_option='None',
        query_params={
        },
        label=_('Clusters')
    )
    
    software_id = DynamicModelMultipleChoiceField(
        queryset=Software.objects.all(),
        required=False,
        null_option='None',
        label=_('Software')
    )
    
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'group_id': '$tenant_group_id'
        },
        label=_('Tenant')
    )
    
    tenant_group_id = DynamicModelChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        null_option='None',
        label=_('Tenant Group')
    )

    tag = TagFilterField(model)

    
class InstalledApplicationCSVForm(NetBoxModelImportForm):

    status = CSVChoiceField(
        choices=InstalledApplicationStatusChoices,
        help_text=_('Status'),
        required=False,
    )
    
    tenant_group = CSVModelChoiceField(
        label=_('Tenant Group'),
        queryset=TenantGroup.objects.all(),
        required=True,
        to_field_name='name',
        help_text=('Name of assigned tenant group')
    )
    
    tenant = CSVModelChoiceField(
        label=_('Tenant'),
        queryset=Tenant.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned tenant')
    )
    
    software = CSVModelChoiceField(
        label=_('Software'),
        queryset=Software.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned software')
    )
    
    cluster_group = CSVModelChoiceField(
        label=_('Cluster Groups'),
        queryset=ClusterGroup.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned cluster group')
    )
    
    cluster = CSVModelMultipleChoiceField(
        label=_('Clusters'),
        queryset=Cluster.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned cluster')
    )
    
    virtual_machine = CSVModelMultipleChoiceField(
        label=_('Virtual Machines'),
        queryset=VirtualMachine.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned virtual machine')
    )
    
    device = CSVModelMultipleChoiceField(
        label=_('Devices'),
        queryset=Device.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned device')
    )

    class Meta:
        model = InstalledApplication
        fields = ['name' ,'status', 'description', 'version', 'software', 'status_date', 'url', 'tenant', 'tenant_group', 'virtual_machine', 'cluster', 'device', 'tags', 'comments' ]
        default_return_url = 'plugins:adestis_netbox_applications:InstalledApplication_list'


    