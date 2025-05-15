from adestis_netbox_applications.models import InstalledApplication
from adestis_netbox_applications.models.software import Software
from adestis_netbox_applications.filtersets import *
from adestis_netbox_applications.filtersets.software import *
from netbox.api.viewsets import NetBoxModelViewSet
from .serializers import InstalledApplicationSerializer, SoftwareSerializer

class InstalledApplicationViewSet(NetBoxModelViewSet):
    queryset = InstalledApplication.objects.prefetch_related(
        'tags', 'virtual_machine', 'device', 'cluster', 'cluster_group',
    )
    serializer_class = InstalledApplicationSerializer
    filterset_class = InstalledApplicationFilterSet
    
class SoftwareViewSet(NetBoxModelViewSet):
    queryset = Software.objects.prefetch_related(
        'tags'
    )

    serializer_class = SoftwareSerializer
    filterset_class = SoftwareFilterSet