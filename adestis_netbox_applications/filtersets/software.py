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

__all__ = (
    'SoftwareFilterSet',
)

class SoftwareFilterSet(NetBoxModelFilterSet):
    
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
        fields = ['id', 'status', 'name', 'url', 'manufacturer']
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(status__icontains=value) |
            Q(manufacturer__name__icontains=value) |
            Q(url__icontains=value)
        ).distinct()
