from adestis_netbox_applications.models import Software
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
from adestis_netbox_applications.models.software_version import *

__all__ = (
    'SoftwareFilterSet',
)

class SoftwareFilterSet(NetBoxModelFilterSet):
    
    parent_software = django_filters.ModelMultipleChoiceFilter(
        queryset=Software.objects.all(),
        required = False, 
        field_name = 'parent_software',
        label=_('Parent Software (name)')
    )
    
    contact = django_filters.ModelMultipleChoiceFilter(
        field_name='contact',
        queryset=Contact.objects.all()
    )
    
    contact_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ContactGroup.objects.all(),
        label=_('Container Group (ID)'),
    )
    
    contact_group = DynamicModelMultipleChoiceField(
        queryset=ContactGroup.objects.all(),
        required=False,
        null_option='None',
        label=_('Container Group')
    )
    
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Manufacturer.objects.all(),
        label=_('Manufacturer (ID)'),
    )
    
    manufacturer = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        to_field_name='manufacturer',
        label=_('Manufacturer (name)'),
    )
    


    class Meta:
        model = Software
        fields = ['id', 'status', 'name', 'parent_software', 'url', 'manufacturer',  'contact', 'contact_group', 'approval_status', 'approval_info',]
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(status__icontains=value) |
            Q(manufacturer__name__icontains=value) |
            Q(url__icontains=value) |
            Q(contact__name__icontains=value) |
            Q(contact_group__name__icontains=value) |
            Q(parent_software__name__icontains=value) |
            # Q(software_version__name__icontains=value) |
            Q(approval_status__icontains=value) |
            Q(approval_info__icontains=value)
        ).distinct()
