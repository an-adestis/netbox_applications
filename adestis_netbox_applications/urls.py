from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from adestis_netbox_applications.models.application import *
from adestis_netbox_applications.models.software import *
from adestis_netbox_applications.models.application_types import *
from adestis_netbox_applications.views.application import *
from adestis_netbox_applications.views.software import *
from adestis_netbox_applications.views.application_types import *
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
    
     # path('applications/certificates/', InstalledApplicationAffectedCertificateView.as_view(),
     #     name='certificateapplications_list'),
    
    #Software
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
    
    
    #Application Types
    path('application_types/', InstalledApplicationTypesListView.as_view(),
         name='installedapplicationtypes_list'),
    path('application_types/add/', InstalledApplicationTypesEditView.as_view(),
         name='installedapplicationtypes_add'),
    path('application_types/delete/', InstalledApplicationTypesBulkDeleteView.as_view(),
         name='installedapplicationtypes_bulk_delete'),
    path('application_types/edit/', InstalledApplicationTypesBulkEditView.as_view(),
         name='installedapplicationtypes_bulk_edit'),
    path('application_types/import/', InstalledApplicationTypesBulkImportView.as_view(),
         name='installedapplicationtypes_bulk_import'),
    path('application_types/<int:pk>/',
         InstalledApplicationTypesView.as_view(), name='installedapplicationtypes'),
    path('application_types/<int:pk>/',
         include(get_model_urls("adestis_netbox_applications", "installedapplicationtypes"))),
    path('application_types/<int:pk>/edit/',
         InstalledApplicationTypesEditView.as_view(), name='installedapplicationtypes_edit'),
    path('application_types/<int:pk>/delete/',
         InstalledApplicationTypesDeleteView.as_view(), name='installedapplicationtypes_delete'),
    path('application_types/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='installedapplicationtypes_changelog', kwargs={
        'model': InstalledApplicationTypes
    }),
    

)
