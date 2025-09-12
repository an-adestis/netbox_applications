from adestis_netbox_applications.models import InstalledApplication
from adestis_netbox_applications.models.software import Software
from adestis_netbox_applications.models.application_types import InstalledApplicationTypes
from adestis_netbox_applications.filtersets.application_types import InstalledApplicationTypes
from adestis_netbox_applications.filtersets import *
from adestis_netbox_applications.filtersets.software import *
from netbox.api.viewsets import NetBoxModelViewSet
from .serializers import InstalledApplicationSerializer, SoftwareSerializer, InstalledApplicationTypesSerializer

class InstalledApplicationViewSet(NetBoxModelViewSet):
    queryset = InstalledApplication.objects.order_by('name') 
    serializer_class = InstalledApplicationSerializer
    filterset_class = InstalledApplicationFilterSet
    
class SoftwareViewSet(NetBoxModelViewSet):
    queryset = Software.objects.prefetch_related(
        'tags'
    )

    serializer_class = SoftwareSerializer
    filterset_class = SoftwareFilterSet
    
class InstalledApplicationTypesViewSet(NetBoxModelViewSet):
    queryset = InstalledApplicationTypes.objects.prefetch_related(
        'tags'
    )

    serializer_class = InstalledApplicationTypesSerializer
    filterset_class = InstalledApplicationTypesFilterSet