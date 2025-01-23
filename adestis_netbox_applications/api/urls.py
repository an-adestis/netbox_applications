from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'adestis_netbox_applications'

router = NetBoxRouter()
router.register('applications', views.ApplicationViewSet)

urlpatterns = router.urls
