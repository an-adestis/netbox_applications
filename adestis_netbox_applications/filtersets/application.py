from adestis_netbox_applications.models.application import *
from adestis_netbox_applications.models.software import *
from netbox.filtersets import NetBoxModelFilterSet

from django.db.models import Q
from django.utils.translation import gettext as _

from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
)
import django_filters
from django import forms
from utilities.forms.widgets import DatePicker
from utilities.filters import TreeNodeMultipleChoiceFilter
from virtualization.models import *
from tenancy.models import *
from dcim.models import *

from ipam.api.serializers import *
from ipam.api.field_serializers import *

__all__ = (
    'InstalledApplicationFilterSet',
)

class InstalledApplicationFilterSet(NetBoxModelFilterSet):
    
    status_date = forms.DateField(
        required=False,
        widget=DatePicker
    )
    
    url = forms.URLField(
        required=False
    )
    
    version = forms.CharField(
        required=False
    )
    
    cluster_group = DynamicModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=False,
        label=_('Cluster group (name)')
    )   
    
    cluster = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label=_('Cluster (name)')
    )
    
    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required = False,
        label=_('Device (ID)'),
    )
    
    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required= False,
        to_field_name='name',
        label=_('Device (name)'),
    )

    virtual_machine = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label=_('Virtual machine (name)')
    )
    
    tenant = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant (ID)'),
    )
    
    tenant_group = DynamicModelMultipleChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        label=_('Tenant Group (name)'),
    )
    
    # software_id = DynamicModelMultipleChoiceField(
    #     queryset=Software.objects.all(),
    #     required=False,
    #     label=_('Software (ID)'),
    # )
    
    software = DynamicModelMultipleChoiceField(
        queryset=Software.objects.all(),
        required = False,
        to_field_name='software',
        label=_('Software (name)'),
    )

    class Meta:
        model = InstalledApplication
        fields = ['id', 'status', 'status_date', 'name', 'url', 'status_date', 'url', 'version', 'tenant', 'tenant_group', 'virtual_machine', 'device', 'cluster', 'cluster_group', 'software']
    

    # def search(self, queryset, name, value):
    #     if not value.strip():
    #         return queryset


