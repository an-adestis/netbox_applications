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
    
    virtual_machine = django_filters.ModelMultipleChoiceFilter(
        field_name='virtual_machine',
        queryset=VirtualMachine.objects.all()
    )
    
    cluster_group = django_filters.ModelMultipleChoiceFilter(
        field_name='cluster_group',
        queryset=ClusterGroup.objects.all()
    )
    
    cluster = django_filters.ModelMultipleChoiceFilter(
        field_name='cluster',
        queryset=Cluster.objects.all()
    )
    
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device',
        queryset=Device.objects.all()
    )
    
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        label=_('Tenant (ID)'),
    )
    
    tenant = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        required=False,
        field_name='tenant__name',
        to_field_name='tenant',
        label=_('Tenant (name)'),
    )
    
    tenant_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=TenantGroup.objects.all(),
        label=_('Tenant (ID)'),
    )
    
    tenant_group = django_filters.ModelMultipleChoiceFilter(
        queryset=TenantGroup.objects.all(),
        required=False,
        field_name='tenant_group__name',
        label=_('Tenant Group (name)'),
    )
    
    software_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Software.objects.all(),
        label=_('Software (ID)'),
    )
    
    software = django_filters.ModelMultipleChoiceFilter(
        queryset=Software.objects.all(),
        required = False,
        field_name='software__name',
        label=_('Software (name)'),
    )

    class Meta:
        model = InstalledApplication
        fields = ('id', 'status', 'status_date', 'name', 'url', 'status_date', 'url', 'version', 'tenant', 'tenant_group', 'tenant_group_id', 'virtual_machine', 'device', 'cluster', 'cluster_group', 'software')
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(system_url__icontains=value) |
            Q(system_status__icontains=value)
        )