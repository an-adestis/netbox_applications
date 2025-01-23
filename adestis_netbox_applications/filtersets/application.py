from adestis_netbox_applications.models import Application
from netbox.filtersets import NetBoxModelFilterSet
from django.db.models import Q
from django.utils.translation import gettext as _

__all__ = (
    'ApplicationFilterSet',
)

class ApplicationFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = Application
        fields = ['id', 'status']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter( Q(status__icontains=value) )
