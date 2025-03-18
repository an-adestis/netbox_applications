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
    
    manufacturer = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        to_field_name='manufacturer',
        label=_('Manufacturer (name)'),
    )

    class Meta:
        model = Software
        fields = ['id', 'status', 'name', 'url']
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

