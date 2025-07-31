from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'adestis_netbox_applications'

router = NetBoxRouter()
router.register('applications', views.InstalledApplicationViewSet)
router.register('software', views.SoftwareViewSet)
router.register('installedapplication_types', views.InstalledApplicationTypesViewSet)

urlpatterns = router.urls
