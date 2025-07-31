from adestis_netbox_applications.models import *
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
    'InstalledApplicationTypesFilterSet',
)

class TaggableManagerFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    def filter(self, qs, value):
        if value:
            return qs.filter(tags__name__in=value)
        return qs

class InstalledApplicationTypesFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = InstalledApplicationTypes
        fields = ['id', 'name', 'tags']
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

