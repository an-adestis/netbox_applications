from rest_framework import serializers
from adestis_netbox_applications.models import *
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.models import *
from tenancy.api.serializers import *
from dcim.api.serializers import *
from dcim.models import *
from virtualization.api.serializers import *

class InstalledApplicationSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:adestis_netbox_applications-api:installedapplication-detail'
    )

    class Meta:
        model = InstalledApplication
        fields = ('id', 'tags', 'custom_fields', 'display', 'url', 'created', 'last_updated',
                  'custom_field_data', 'status', 'status_date', 'comments', 'tenant', 'tenant_group', 'cluster',  'virtual_machine',  'description', 'software' )
        brief_fields = ('id', 'tags', 'custom_fields', 'display', 'url', 'created', 'last_updated',
                        'custom_field_data', 'status', 'status_date', 'comments', 'tenant', 'tenant_group', 'cluster',  'virtual_machine',  'description', 'software' )

