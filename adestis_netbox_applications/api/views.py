from adestis_netbox_applications.models import InstalledApplication
from adestis_netbox_applications.filtersets import *
from netbox.api.viewsets import NetBoxModelViewSet
from .serializers import InstalledApplicationSerializer

class InstalledApplicationViewSet(NetBoxModelViewSet):
    queryset = InstalledApplication.objects.prefetch_related(
        'tags'
    )
    serializer_class = InstalledApplicationSerializer
    filterset_class = InstalledApplicationFilterSet