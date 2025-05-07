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
    'DeviceAssignmentForm',
    'ClusterAssignmentForm',
    'ClusterGroupAssignmentForm',
    'VirtualMachineAssignmentForm',
)

class InstalledApplicationForm(NetBoxModelForm):

    fieldsets = (
        FieldSet('name', 'description', 'url', 'tags', 'status', 'status_date',  name=_('Application')),
        FieldSet('tenant_group', 'tenant',  name=_('Tenant')), 
        FieldSet('virtual_machine', 'cluster_group', 'cluster', name=_('Virtualization')),   
        FieldSet('device', name=_('Device')),
        FieldSet('software', name=('Software'))
    )



    class Meta:
        model = InstalledApplication
        fields = ['name', 'description', 'url', 'tags', 'status', 'status_date', 'tenant', 'virtual_machine', 'device', 'cluster_group', 'cluster', 'tenant_group', 'comments', 'software']
        
        help_texts = {
            'status': "Example text",
        }
        
        widgets = {
            'status_date': DatePicker(),
        }
   
   
class DeviceAssignmentForm(forms.ModelForm):

    device = DynamicModelChoiceField(
        queryset=InstalledApplication.objects.all(),
        required=True,
    )
    
    class Meta:
        model = DeviceAssignment
        fields = ["application_type", "application_id", "device"]
        widgets = {
            "application_type": forms.HiddenInput(),
            "application_id": forms.HiddenInput(),
        }    
        
        
class ClusterAssignmentForm(forms.ModelForm):

    cluster = DynamicModelChoiceField(
        queryset=InstalledApplication.objects.all(),
        required=True,
    )
    
    class Meta:
        model = ClusterAssignment
        fields = ["application_type", "application_id", "cluster"]
        widgets = {
            "application_type": forms.HiddenInput(),
            "application_id": forms.HiddenInput(),
        } 
        
        
class ClusterGroupAssignmentForm(forms.ModelForm):

    cluster_group = DynamicModelChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=True,
    )
    
    class Meta:
        model = ClusterGroupAssignment
        fields = ["application_type", "application_id", "cluster_group"]
        widgets = {
            "application_type": forms.HiddenInput(),
            "application_id": forms.HiddenInput(),
        } 
        
        
class VirtualMachineAssignmentForm(forms.ModelForm):

    virtual_machine = DynamicModelChoiceField(
        queryset=InstalledApplication.objects.all(),
        required=True,
    )
    
    class Meta:
        model = VirtualMachineAssignment
        fields = ["application_type", "application_id", "virtual_machine"]
        widgets = {
            "application_type": forms.HiddenInput(),
            "application_id": forms.HiddenInput(),
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
    
    virtual_machine = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required = False,
        label = ("Virtual Machines"),
        null_option='None'
    )

    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required = False,
        label =_("Device"),
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
    
    # cluster_group = DynamicModelChoiceField(
    #     queryset=ClusterGroup.objects.all(),
    #     required = False,
    #     label=_("Cluster Group")
    # )
    
    cluster = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required = False,
        label=_("Cluster"),
        null_option='None'
    )
    
    model = InstalledApplication

    fieldsets = (
        FieldSet('name', 'description', 'url', 'tags', 'status', 'status_date', 'comments', name=_('Application')),
        FieldSet('tenant_group', 'tenant', name=_('Tenant')),
        FieldSet('virtual_machine', 'cluster', name=_('Virtualization')),
        FieldSet('device', name=_('Device')),
        FieldSet('software', name=_('Software'))
    )

    nullable_fields = [
         'add_tags', 'remove_tags', 'description', ''
    ]
    
class InstalledApplicationFilterForm(NetBoxModelFilterSetForm):
    
    model = InstalledApplication

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'url', 'tag', 'status', 'status_date', name=_('Application')),
        FieldSet('tenant_group_id', 'tenant_id', name=_('Tenant')),
        FieldSet('cluster_id', 'virtual_machine_id', name=_('Virtualization')),
        FieldSet('device_id', name=_('Device')),
        FieldSet('software_id', name=_('Software'))
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
        label=_('Device')
    )
    
    virtual_machine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'cluster_id': '$cluster_id',
            'device_id': '$device_id',
        },
        label=_('Virtual Machine')
    )
    
    # cluster_group_id = DynamicModelMultipleChoiceField(
    #     queryset=ClusterGroup.objects.all(),
    #     required=False,
    #     null_option='None',
    #     label=_('Cluster Group')
    # )

    cluster_id = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        null_option='None',
        query_params={
        },
        label=_('Cluster')
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
        help_text=('Assigned tenant group')
    )
    
    tenant = CSVModelChoiceField(
        label=_('Tenant'),
        queryset=Tenant.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Assigned tenant')
    )
    
    software = CSVModelChoiceField(
        label=_('Software'),
        queryset=Software.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Assigned software')
    )
    
    # cluster_group = CSVModelChoiceField(
    #     label=_('Cluster Group'),
    #     queryset=ClusterGroup.objects.all(),
    #     required=True,
    #     to_field_name='name',
    #     help_text=_('Assigned cluster group')
    # )
    
    cluster = CSVModelMultipleChoiceField(
        label=_('Cluster'),
        queryset=Cluster.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Assigned cluster')
    )
    
    virtual_machine = CSVModelMultipleChoiceField(
        label=_('Virtual Machine'),
        queryset=VirtualMachine.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Assigned virtual machine')
    )
    
    device = CSVModelMultipleChoiceField(
        label=_('Device'),
        queryset=Device.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Assigned device')
    )

    class Meta:
        model = InstalledApplication
        fields = ['name' ,'status', 'status_date', 'url', 'tenant', 'tenant_group', 'virtual_machine', 'cluster', 'device', 'description',  'tags', 'comments', 'software']
        default_return_url = 'plugins:adestis_netbox_applications:InstalledApplication_list'


    