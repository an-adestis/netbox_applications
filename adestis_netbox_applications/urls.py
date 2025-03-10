from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from adestis_netbox_applications.models import *
from adestis_netbox_applications.views import *
from django.urls import include
from utilities.urls import get_model_urls

urlpatterns = (

    # Applications
    path('applications/', InstalledApplicationListView.as_view(),
         name='installedapplication_list'),
    path('applications/add/', InstalledApplicationEditView.as_view(),
         name='installedapplication_add'),
    path('applications/delete/', InstalledApplicationBulkDeleteView.as_view(),
         name='installedapplication_bulk_delete'),
    path('applications/edit/', InstalledApplicationBulkEditView.as_view(),
         name='installedapplication_bulk_edit'),
    path('applications/import/', InstalledApplicationBulkImportView.as_view(),
         name='installedapplication_bulk_import'),
    path('applications/<int:pk>/',
         InstalledApplicationView.as_view(), name='installedapplication'),
    path('applications/<int:pk>/',
         include(get_model_urls("adestis_netbox_applications", "installedapplication"))),
    path('applications/<int:pk>/edit/',
         InstalledApplicationEditView.as_view(), name='installedapplication_edit'),
    path('applications/<int:pk>/delete/',
         InstalledApplicationDeleteView.as_view(), name='installedapplication_delete'),
    path('applications/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='installedapplication_changelog', kwargs={
        'model': InstalledApplication
    }),

)
