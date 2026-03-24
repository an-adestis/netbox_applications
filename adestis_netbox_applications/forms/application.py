from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_applications.models.application import InstalledApplication, DeviceAssignment, InstalledApplicationStatusChoices
from adestis_netbox_applications.models.software import *
from adestis_netbox_applications.models.application_types import *
from adestis_netbox_certificate_management.models import Certificate
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    TagFilterField,
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
import django_filters
from utilities.forms import ConfirmationForm
from utilities.forms.widgets import DatePicker
from tenancy.models import Tenant, TenantGroup, Contact, ContactGroup
from dcim.models import *
from virtualization.models import *
from adestis_netbox_applications.models.software import *

__all__ = (
    'InstalledApplicationForm',
    'InstalledApplicationFilterForm',
    'InstalledApplicationBulkEditForm',
    'InstalledApplicationCSVForm',
    'InstalledApplicationAssignDeviceForm',
    'InstalledApplicationAssignClusterForm',
    'InstalledApplicationAssignClusterGroupForm',
    'InstalledApplicationAssignVirtualMachineForm',
    'InstalledApplicationAssignCertificateForm',
    'InstalledApplicationRemoveDevice',
    'InstalledApplicationRemoveCluster',
    'InstalledApplicationRemoveClusterGroup',
    'InstalledApplicationRemoveVirtualMachine',
    'InstalledApplicationRemoveCertificate',
)

class InstalledApplicationForm(NetBoxModelForm):
    
    tenant_group = DynamicModelChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        null_option='None',
    )

    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        query_params={
            'group_id': '$tenant_group'
        },
    )

    cluster_group = DynamicModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=False,
        help_text=_("Cluster Group"),
    )

    cluster = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        query_params={
            'group_id': '$cluster_group',
        },
        help_text=_("Cluster"),
    )
    
    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'cluster_id': '$cluster',
        },
        help_text=_("Device"),
    )
    
    virtual_machine = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'cluster_id': '$cluster',
            'device_id': '$device',
        },
        help_text=_("Virtual Machine"),
    )

    fieldsets = (
        FieldSet('name', 'application_types', 'description', 'software', 'version', 'url', 'tags', 'status', 'status_date',  name=_('Application')),
        FieldSet('tenant_group', 'tenant',  name=_('Tenant')), 
        FieldSet('cluster_group', 'cluster', 'virtual_machine',  name=_('Virtualization')),   
        FieldSet('device', name=_('Device'))
    )

    class Meta:
        model = InstalledApplication
        fields = ['name', 'description', 'url', 'tags', 'status', 'status_date', 'tenant', 'virtual_machine', 'device', 'cluster_group', 'cluster', 'tenant_group', 'comments', 'software', 'application_types', 'version']
        
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
        initial_params={
            'tenants': '$tenant'
        }
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required = False,
        label=_("Tenant"),
        query_params={
            'group_id': '$tenant_group'
        },
    )
    
    software = DynamicModelChoiceField(
        queryset=Software.objects.all(),
        required= False,
        label=_('Software'),
    )
    
    application_types = DynamicModelChoiceField(
        queryset=InstalledApplicationTypes.objects.all(),
        required= False,
        label=_('Application Types'),
    )
    
    cluster_group = DynamicModelChoiceField(
        queryset=ClusterGroup.objects.all(),
        required = False,
        label=_("Cluster Groups"),
        initial_params={
            'clusters': '$cluster'
        }
    )
    
    cluster = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required = False,
        label=_("Clusters"),
        query_params={
            'group_id': '$cluster_group',
        },
        null_option='None'
    )
    
    model = InstalledApplication

    fieldsets = (
        FieldSet('name', 'application_types', 'description', 'software', 'version', 'url', 'tags', 'status', 'status_date', 'comments', name=_('Application')),
        FieldSet('tenant_group', 'tenant', name=_('Tenant')),
        FieldSet('cluster_group', 'cluster', 'virtual_machine', name=_('Virtualization')),
        FieldSet('device', name=_('Device'))
    )

    nullable_fields = [
         'add_tags', 'remove_tags', 'description', ''
    ]
    
class InstalledApplicationFilterForm(NetBoxModelFilterSetForm):
    
    model = InstalledApplication

    fieldsets = (
        FieldSet('name', 'application_types_id', 'description', 'version', 'software_id', 'url', 'tags', 'status', 'status_date',  name=_('Application')),
        FieldSet('tenant_group_id', 'tenant_id',  name=_('Tenant')), 
        FieldSet('cluster_group', 'cluster', 'virtual_machine', name=_('Virtualization')),   
        FieldSet('device', name=_('Device'))
    )

    index = forms.IntegerField(
        required=False
    )
    
    name = forms.CharField(
        max_length=200,
        required=False
    )
    
    status_date = forms.DateField(
        required=False
    )
    
    version = forms.CharField(
        required=False
    )
    
    url = forms.URLField(
        required=False
    )

    status = forms.MultipleChoiceField(
        choices=InstalledApplicationStatusChoices,
        required=False,
        label=_('Status')
    )
    
    virtual_machine = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        label=_('Virtual Machine'),
        required=False,
    )
    
    cluster_group = DynamicModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        label=_('Cluster Group'),
        required=False,
    )
    
    cluster = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        label=_('Cluster'),
        query_params={
            'group_id': '$cluster_group',
        },
        required=False,
    )
    
    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        label=_('Device'),
        required=False,
    )
    
    software_id = DynamicModelMultipleChoiceField(
        queryset=Software.objects.all(),
        required=False,
        label=_('Software')
    )
    
    application_types_id = DynamicModelMultipleChoiceField(
        queryset=InstalledApplicationTypes.objects.all(),
        required=False,
        label=_('Application Types')
    )
    
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        query_params={
            'group_id': '$tenant_group_id'
        },
        label=_('Tenant')
    )
    
    tenant_group_id = DynamicModelMultipleChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
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
        required=False,
        to_field_name='name',
        help_text=('Name of assigned tenant group')
    )
    
    tenant = CSVModelChoiceField(
        label=_('Tenant'),
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of assigned tenant')
    )
    
    software = CSVModelChoiceField(
        label=_('Software'),
        queryset=Software.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of assigned software')
    )
    
    application_types = CSVModelChoiceField(
        label=_('Application Types'),
        queryset=InstalledApplicationTypes.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of assigned application type')
    )
    
    cluster_group = CSVModelMultipleChoiceField(
        label=_('Cluster Groups'),
        queryset=ClusterGroup.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of assigned cluster group')
    )
    
    cluster = CSVModelMultipleChoiceField(
        label=_('Clusters'),
        queryset=Cluster.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of assigned cluster')
    )
    
    virtual_machine = CSVModelMultipleChoiceField(
        label=_('Virtual Machines'),
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of assigned virtual machine')
    )
    
    device = CSVModelMultipleChoiceField(
        label=_('Devices'),
        queryset=Device.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of assigned device')
    )

    class Meta:
        model = InstalledApplication
        fields = ['name', 'application_types', 'status', 'description', 'version', 'software', 'status_date', 'url', 'tenant', 'tenant_group', 'virtual_machine', 'cluster', 'device', 'tags', 'comments' ]
        default_return_url = 'plugins:adestis_netbox_applications:InstalledApplication_list'

class InstalledApplicationAssignDeviceForm(forms.Form):
    
    device = DynamicModelMultipleChoiceField(
        label=_('Devices'),
        queryset=Device.objects.all()
    )

    class Meta:
        fields = [
            'device',
        ]

    def __init__(self, installedapplication,*args, **kwargs):

        self.installedapplication = installedapplication

        self.device = DynamicModelMultipleChoiceField(
            label=_('Devices'),
            queryset=Device.objects.all()
        )        

        super().__init__(*args, **kwargs)

        self.fields['device'].choices = []
        
class InstalledApplicationAssignClusterForm(forms.Form):
    
    cluster_group = DynamicModelMultipleChoiceField(
            label=_('Cluster Group'),
            queryset= ClusterGroup.objects.all()
        )
    
    cluster = DynamicModelMultipleChoiceField(
        label=_('Clusters'),
        queryset=Cluster.objects.all(),
        query_params={
            'group_id': '$cluster_group',
        },)

    class Meta:
        fields = [
            'cluster_group', 'cluster',
        ]

    def __init__(self, installedapplication,*args, **kwargs):

        self.installedapplication = installedapplication
        
        self.cluster_group = DynamicModelMultipleChoiceField(
            label=_('Cluster Group'),
            queryset= ClusterGroup.objects.all()
        )

        self.cluster = DynamicModelMultipleChoiceField(
            label=_('Clusters'),
            queryset=Cluster.objects.all(),
            query_params={
            'group_id': '$cluster_group',
        },
        )        

        super().__init__(*args, **kwargs)

        self.fields['cluster'].choices = []
        
class InstalledApplicationAssignClusterGroupForm(forms.Form):
    
    cluster_group = DynamicModelMultipleChoiceField(
        label=_('Cluster Groups'),
        queryset=ClusterGroup.objects.all()
    )

    class Meta:
        fields = [
            'cluster_group',
        ]

    def __init__(self, installedapplication,*args, **kwargs):

        self.installedapplication = installedapplication

        self.cluster_group = DynamicModelMultipleChoiceField(
            label=_('Cluster Group'),
            queryset=ClusterGroup.objects.all()
        )        

        super().__init__(*args, **kwargs)

        self.fields['cluster_group'].choices = []
        
class InstalledApplicationAssignVirtualMachineForm(forms.Form):
    
    virtual_machine = DynamicModelMultipleChoiceField(
        label=_('Virtual Machines'),
        queryset=VirtualMachine.objects.all()
    )

    class Meta:
        fields = [
            'virtual_machine',
        ]

    def __init__(self, installedapplication,*args, **kwargs):

        self.installedapplication = installedapplication

        self.virtual_machine = DynamicModelMultipleChoiceField(
            label=_('Virtual Machines'),
            queryset=VirtualMachine.objects.all()
        )        

        super().__init__(*args, **kwargs)

        self.fields['virtual_machine'].choices = []
        
class InstalledApplicationAssignCertificateForm(forms.Form):
    certificate = DynamicModelMultipleChoiceField(
        label=_('Certificate'),
        queryset=Certificate.objects.all()
    )

    class Meta:
        fields = [
            'certificate',
        ]

    def __init__(self, installedapplication,*args, **kwargs):

        self.installedapplication = installedapplication

        self.certificate = DynamicModelMultipleChoiceField(
            label=_('Certificate'),
            queryset=Certificate.objects.all()
        )        

        super().__init__(*args, **kwargs)

        self.fields['certificate'].choices = []
    
class InstalledApplicationRemoveDevice(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Device.objects.all(),
        widget=forms.MultipleHiddenInput()
    ) 
    
class InstalledApplicationRemoveCluster(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    
class InstalledApplicationRemoveClusterGroup(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    
class InstalledApplicationRemoveVirtualMachine(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    
class InstalledApplicationRemoveCertificate(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Certificate.objects.all(),
        widget=forms.MultipleHiddenInput()
    )