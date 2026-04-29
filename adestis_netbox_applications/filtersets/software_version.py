from adestis_netbox_applications.models import Software, SoftwareVersion
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
    'SoftwareVersionFilterSet',
)

class SoftwareVersionFilterSet(NetBoxModelFilterSet):
    
    software = django_filters.ModelMultipleChoiceFilter(
        queryset=Software.objects.all(),
        required = False, 
        field_name = 'software',
        label=_('Software (name)')
    )

    class Meta:
        model = SoftwareVersion
        fields = ['id', 'name', 'software', 'url', 'version', 'approval_status', 'approval_info',]
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |

            Q(version__icontains=value) |
            Q(url__icontains=value) |

            Q(software__name__icontains=value) |
            Q(approval_status__icontains=value) |
            Q(approval_info__icontains=value)
        ).distinct()
