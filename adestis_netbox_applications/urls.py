from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from adestis_netbox_applications.models import *
from adestis_netbox_applications.views import *
from django.urls import include
from utilities.urls import get_model_urls

urlpatterns = (

    # Applications
    path('applications/', ApplicationListView.as_view(),
         name='application_list'),
    path('applications/add/', ApplicationEditView.as_view(),
         name='application_add'),
    path('applications/delete/', ApplicationBulkDeleteView.as_view(),
         name='application_bulk_delete'),
    path('applications/edit/', ApplicationBulkEditView.as_view(),
         name='application_bulk_edit'),
    path('applications/import/', ApplicationBulkImportView.as_view(),
         name='application_import'),
    path('applications/<int:pk>/',
         ApplicationView.as_view(), name='application'),
    path('applications/<int:pk>/',
         include(get_model_urls("adestis_netbox_applications", "application"))),
    path('applications/<int:pk>/edit/',
         ApplicationEditView.as_view(), name='application_edit'),
    path('applications/<int:pk>/delete/',
         ApplicationDeleteView.as_view(), name='application_delete'),
    path('applications/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='application_changelog', kwargs={
        'model': Application
    }),

)
