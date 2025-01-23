from adestis_netbox_applications.models import Application
from adestis_netbox_applications.filtersets import *
from netbox.api.viewsets import NetBoxModelViewSet
from .serializers import ApplicationSerializer

class ApplicationViewSet(NetBoxModelViewSet):
    queryset = Application.objects.prefetch_related(
        'tags'
    )

    serializer_class = ApplicationSerializer
    filterset_class = ApplicationFilterSet