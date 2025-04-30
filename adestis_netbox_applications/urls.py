from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from adestis_netbox_applications.models import *
from adestis_netbox_applications.models.software import *
from adestis_netbox_applications.views import *
from adestis_netbox_applications.views.software import *
from django.urls import include
from utilities.urls import get_model_urls

app_name = 'adestis_netbox_applications'

urlpatterns = (

    # Applications
    path('applications/', InstalledApplicationView.as_view(),
         name='installedapplication_list'),
    path('applications/devices/', DeviceAffectedInstalledApplicationView.as_view(),
         name='applicationdevices_list'),
    path('applications/add/', InstalledApplicationEditView.as_view(),
         name='installedapplication_add'),
    path('applications/delete/', InstalledApplicationBulkDeleteView.as_view(),
         name='installedapplication_bulk_delete'),
    path('applications/edit/', InstalledApplicationBulkEditView.as_view(),
         name='installedapplication_bulk_edit'),
    path('applications/import/', InstalledApplicationBulkImportView.as_view(),
         name='installedapplication_bulk_import'),
    path('applications/<int:pk>/',
         InstalledApplicationListView.as_view(), name='installedapplication'),
    path('applications/<int:pk>/',
         include(get_model_urls("adestis_netbox_applications", "installedapplication"))),
    path('applications/<int:pk>/edit/',
         InstalledApplicationEditView.as_view(), name='installedapplication_edit'),
    path('applications/<int:pk>/delete/',
         InstalledApplicationDeleteView.as_view(), name='installedapplication_delete'),
    path('applications/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='installedapplication_changelog', kwargs={
        'model': InstalledApplication
    }),
    
    path('software/', SoftwareListView.as_view(),
         name='software_list'),
    path('software/add/', SoftwareEditView.as_view(),
         name='software_add'),
    path('software/delete/', SoftwareBulkDeleteView.as_view(),
         name='software_bulk_delete'),
    path('software/edit/', SoftwareBulkEditView.as_view(),
         name='software_bulk_edit'),
    path('software/import/', SoftwareBulkImportView.as_view(),
         name='software_bulk_import'),
    path('software/<int:pk>/',
         SoftwareView.as_view(), name='software'),
    path('software/<int:pk>/',
         include(get_model_urls("adestis_netbox_applications", "software"))),
    path('software/<int:pk>/edit/',
         SoftwareEditView.as_view(), name='software_edit'),
    path('software/<int:pk>/delete/',
         SoftwareDeleteView.as_view(), name='software_delete'),
    path('software/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='software_changelog', kwargs={
        'model': Software
    }),

)
