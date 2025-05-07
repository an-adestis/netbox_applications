from rest_framework import serializers
from adestis_netbox_applications.models import *
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
                  'custom_field_data', 'status', 'status_date', 'comments', 'tenant', 'tenant_group', 'virtual_machine', 'device', 'cluster', 'description', 'software' )
        brief_fields = ('id', 'tags', 'custom_fields', 'display', 'url', 'created', 'last_updated',
                        'custom_field_data', 'status', 'status_date', 'comments', 'tenant', 'tenant_group','description', 'virtual_machine', 'device', 'cluster', 'software' )

class DeviceAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:adestis_netbox_applications-api:deviceassignment-detail")
    display = serializers.SerializerMethodField('get_display')
    application_type = ContentTypeField(
        queryset=ContentType.objects.all(),
        required=True,
    )
    application = serializers.SerializerMethodField('get_application')
    device = serializers.SlugRelatedField(slug_field="device", queryset=InstalledApplication.objects.all())

    application_id = serializers.IntegerField(source='application.id', write_only=True)

    def validate(self, data):
        application_id = data['application']['id']
        application_type = data['application_type']
        application = application_type.get_object_for_this_type(id=application_id)
        data['application'] = application
        return super().validate(data)

    def get_asset(self, obj):
        if obj.application is None:
            return None
        serializer = get_serializer_for_model(obj.application)
        context = {'request': self.context['request']}
        return serializer(obj.application, context=context, nested=True).data
    
    def get_display(self, obj):
        return obj.name


    class Meta:
        model = DeviceAssignment
        fields = [
            "id",
            "url",
            "display",
            "application_type",
            "application_id",
            "application",
            "device",
        ]
        brief_fields = ['id', 'url', 'display']