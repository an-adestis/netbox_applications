from rest_framework import serializers
from adestis_netbox_applications.models.application import InstalledApplication, DeviceAssignment, ClusterAssignment, ClusterGroupAssignment, VirtualMachineAssignment
from netbox.api.serializers import NetBoxModelSerializer
from django.contrib.contenttypes.models import ContentType
from netbox.api.fields import ChoiceField, ContentTypeField, SerializedPKRelatedField
from tenancy.models import *
from tenancy.api.serializers import *
from dcim.api.serializers import *
from dcim.models import *
from virtualization.api.serializers import *
from utilities.api import get_serializer_for_model

class InstalledApplicationSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:adestis_netbox_applications-api:installedapplication-detail'
    )

    class Meta:
        model = InstalledApplication
        fields = ('id', 'tags', 'custom_fields', 'display', 'url', 'created', 'last_updated',
                  'custom_field_data', 'status', 'status_date', 'comments', 'tenant', 'tenant_group', 'virtual_machine', 'device', 'cluster', 'description', 'software', 'version' )
        brief_fields = ('id', 'tags', 'custom_fields', 'display', 'url', 'created', 'last_updated',
                        'custom_field_data', 'status', 'status_date', 'comments', 'tenant', 'tenant_group','description', 'virtual_machine', 'device', 'cluster', 'software', 'version' )


class DeviceAssignmentSerializer(NetBoxModelSerializer):
    class Meta:
        model = DeviceAssignment
        fields = ('id', 'installed_application', 'device')
        
class ClusterAssignmentSerializer(NetBoxModelSerializer):
    class Meta:
        model = ClusterAssignment
        fields = ('id', 'installed_application', 'cluster')
        
class ClusterGroupAssignmentSerializer(NetBoxModelSerializer):
    class Meta:
        model = ClusterGroupAssignment
        fields = ('id', 'installed_application', 'cluster_group')
        
class VirtualMachineAssignmentSerializer(NetBoxModelSerializer):
    class Meta:
        model = VirtualMachineAssignment
        fields = ('id', 'installed_application', 'virtual_machine')