from adestis_netbox_applications.models.application import *
from adestis_netbox_applications.models.software import *
from adestis_netbox_applications.models.application_types import *
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
    
    contact_id = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        null_option='None',
        label=_('Group')
    )
    
    contact = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        null_option='None',
        label=_('Group')
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
        label=_('Tenant Group (ID)'),
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
    
    application_types_id = django_filters.ModelMultipleChoiceFilter(
        queryset=InstalledApplicationTypes.objects.all(),
        label=_('Application Types (ID)'),
    )
    
    application_types = django_filters.ModelMultipleChoiceFilter(
        queryset=InstalledApplicationTypes.objects.all(),
        required = False,
        field_name='application_types__name',
        label=_('application Types (name)'),
    )

    class Meta:
        model = InstalledApplication
        fields = ('id', 'status', 'status_date', 'name', 'url', 'contact', 'status_date', 'url', 'version', 'tenant', 'tenant_group', 'tenant_group_id', 'virtual_machine', 'device', 'cluster', 'cluster_group', 'software', 'application_types')
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(status__icontains=value) |
            Q(status_date__icontains=value) |
            Q(version__icontains=value) |
            Q(url__icontains=value) |
            Q(contact__name__icontains=value) |
            Q(tenant__name__icontains=value) |
            Q(tenant_group__name__icontains=value) |
            Q(virtual_machine__name__icontains=value) |
            Q(device__name__icontains=value) |
            Q(cluster__name__icontains=value) |
            Q(cluster_group__name__icontains=value) |
            Q(application_types__name__icontains=value) |
            Q(software__name__icontains=value) 
        ).distinct()