from adestis_netbox_applications.models import Application
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
    'ApplicationFilterSet',
)

class ApplicationFilterSet(NetBoxModelFilterSet):
    
    # cluster_group_id = DynamicModelMultipleChoiceField(
    #     queryset=ClusterGroup.objects.all(),
    #     required=False,
    #     label=_('Cluster group (name)')
    # )   
    
    # cluster_id = DynamicModelMultipleChoiceField(
    #     queryset=Cluster.objects.all(),
    #     required=False,
    #     label=_('Cluster (name)')
    # )   

    # virtual_machines_id = DynamicModelMultipleChoiceField(
    #     queryset=VirtualMachine.objects.all(),
    #     required=False,
    #     label=_('Virtual machine (name)'))
   
    class Meta:
        model = Application
        fields = ['id', 'status', 'name', 'url']
        # fields = ['id', 'status', 'name', 'url', 'cluster_group_id', 'cluster_id', 'device', 'virtual_machines_id']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

