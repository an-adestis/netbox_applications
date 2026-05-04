from adestis_netbox_applications.models import Software, SoftwareVersion, InstalledApplication
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
from taggit.managers import TaggableManager

__all__ = (
    'SoftwareVersionFilterSet',
)

class TaggableManagerFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    def filter(self, qs, value):
        if value:
            return qs.filter(tags__name__in=value)
        return qs

class SoftwareVersionFilterSet(NetBoxModelFilterSet):
    
    software = django_filters.ModelMultipleChoiceFilter(
        queryset=Software.objects.all(),
        required = False, 
        field_name = 'software__name',
        label=_('Software (name)')
    )
    
    installedapplication = django_filters.ModelMultipleChoiceFilter(
        queryset=InstalledApplication.objects.all(),
        required = False, 
        field_name='installedapplication__name',
        label=_('Installed Application')
    )

    class Meta:
        model = SoftwareVersion
        fields = ['id', 'name', 'installedapplication', 'software', 'version', 'approval_status', 'approval_info']
        filter_overrides = {
            TaggableManager: {
                'filter_class': TaggableManagerFilter,
                'extra': lambda f: {
                    'label': 'Tags',
                    'help_text': 'Filter by tag names (comma-separated)',
                },
            },
        }
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |

            Q(version__icontains=value) |
            Q(installedapplication__name__icontains=value) |
            Q(software__name__icontains=value) |
            Q(approval_status__icontains=value) |
            Q(approval_info__icontains=value)
        ).distinct()
