from rest_framework import serializers
from adestis_netbox_applications.models import *
from netbox.api.serializers import NetBoxModelSerializer
from netbox.api.fields import *
from tenancy.models import *
from tenancy.api.serializers import *
from dcim.api.serializers import *
from dcim.models import *
from virtualization.api.serializers import *

class SoftwareVersionSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:adestis_netbox_applications-api:softwareversion-detail'
    )
    
    
    software_count=RelatedObjectCountField('software')
    
    class Meta:
        model = SoftwareVersion
        fields = ('id', 'tags', 'custom_fields', 'display', 'created', 'last_updated',
                  'custom_field_data', 'approval_status', 'approval_info', 'software', 'version', 'software_count', 'description', 'installedapplication')
        brief_fields = ('id', 'tags', 'custom_fields', 'display', 'created', 'last_updated',
                        'custom_field_data', 'approval_status', 'approval_info', 'software', 'version', 'software_count', 'description', 'installedapplication')

