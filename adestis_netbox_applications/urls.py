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
    path('applications/', InstalledApplicationListView.as_view(),
         name='installedapplication_list'),
    path('applications/devices/', DeviceAffectedInstalledApplicationView.as_view(),
         name='applicationdevices_list'),
     path('applications/clusters/', ClusterAffectedInstalledApplicationView.as_view(),
         name='applicationclusters_list'),
     path('applications/clustergroups/', ClusterGroupAffectedInstalledApplicationView.as_view(),
         name='applicationclustergroups_list'),
     path('applications/virtualmachines/', VirtualMachineAffectedInstalledApplicationView.as_view(),
         name='applicationvirtualmachines_list'),
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
     path('applications/devices/<int:pk>/delete/',
         DeviceAssignmentDeleteView.as_view(), name='deviceassignment'),
     path('applications/clusters/<int:pk>/delete/',
         ClusterAssignmentDeleteView.as_view(), name='clusterassignment'),
     path('applications/clustergroups/<int:pk>/delete/',
         ClusterGroupAssignmentDeleteView.as_view(), name='clustergroupassignment'),
     path('applications/virtualmachines/<int:pk>/delete/',
         VirtualMachineAssignmentDeleteView.as_view(), name='virtualmachineassignment'),
    path('applications/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='installedapplication_changelog', kwargs={
        'model': InstalledApplication
    }),
    
    #Softwares
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
