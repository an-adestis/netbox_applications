from rest_framework import serializers
from adestis_netbox_applications.models.application_types import *
from netbox.api.serializers import NetBoxModelSerializer
from netbox.api.fields import *
from tenancy.models import *
from tenancy.api.serializers import *
from dcim.api.serializers import *
from dcim.models import *
from virtualization.api.serializers import *

class InstalledApplicationTypesSerializer(NetBoxModelSerializer):
    application_count=RelatedObjectCountField('application_types')

    class Meta:
        model = InstalledApplicationTypes
        fields = ('id', 'tags', 'custom_fields', 'display', 'created', 'last_updated',
                  'custom_field_data', 'application_count', 'slug')
        brief_fields = ('id', 'tags', 'custom_fields', 'display', 'created', 'last_updated',
                        'custom_field_data', 'application_count', 'slug')

