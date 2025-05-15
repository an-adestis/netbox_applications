from adestis_netbox_applications.models.application import *
from adestis_netbox_applications.models.software import *
from netbox.filtersets import NetBoxModelFilterSet

from django.db.models import Q
from django.utils.translation import gettext as _

from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
)
import django_filters
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
    
    cluster_group_id = DynamicModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=False,
        label=_('Cluster group (name)')
    )   
    
    cluster_id = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label=_('Cluster (name)')
    )
    
    device_id = DynamicModelMultipleChoiceField(
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

    virtual_machine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label=_('Virtual machine (name)')
    )
    
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant (ID)'),
    )
    
    tenant = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name='tenant',
        label=_('Tenant (name)'),
    )
    
    software_id = DynamicModelMultipleChoiceField(
        queryset=Software.objects.all(),
        required=False,
        label=_('Software (ID)'),
    )
    
    software = DynamicModelMultipleChoiceField(
        queryset=Software.objects.all(),
        required = False,
        to_field_name='software',
        label=_('Software (name)'),
    )

    class Meta:
        model = InstalledApplication
        fields = ['id', 'status', 'status_date', 'name', 'url']
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset


