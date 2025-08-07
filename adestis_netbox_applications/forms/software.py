from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_applications.models.software import Software, SoftwareStatusChoices
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    TagFilterField,
    CSVModelChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from utilities.forms.widgets import DatePicker
from dcim.models import *
from virtualization.models import *


__all__ = (
    'SoftwareForm',
    'SoftwareFilterForm',
    'SoftwareBulkEditForm',
    'SoftwareCSVForm',
)

class SoftwareForm(NetBoxModelForm):

    fieldsets = (
        FieldSet('name', 'description', 'url', 'tags', 'status',  name=_('Software')),
        FieldSet('manufacturer',  name=_('Virtualization')),   
    )

    class Meta:
        model = Software
        fields = ['name', 'description', 'url', 'tags', 'status',  'manufacturer']
        
        help_texts = {
            'status': "Example text",
        }
        
       

class SoftwareBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Software.objects.all(),
        widget=forms.MultipleHiddenInput, 
    )
    
    name = forms.CharField(
        required=False,
        max_length = 150,
        label=_("Name"),
    )
    
    url = forms.URLField(
        max_length=300,
        required=False,
        label=_("URL")
    )

    status = forms.ChoiceField(
        required=False,
        choices=SoftwareStatusChoices,
    )
    
    
    description = forms.CharField(
        max_length=500,
        required=False,
        label=_("Description"),
    )
    
    model = Software

    fieldsets = (
        FieldSet('name', 'description', 'url', 'tags', 'status', name=_('Software')),
        FieldSet('manufacturer',  name=_('Virtualization')),
    )

    nullable_fields = [
         'add_tags', 'remove_tags', 'description', ''
    ]
    
class SoftwareFilterForm(NetBoxModelFilterSetForm):
    
    model = Software

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'url', 'tag', 'status',  name=_('Software')),
        FieldSet('manufacturer_id',  name=_('Virtualization')),
    )

    index = forms.IntegerField(
        required=False
    )

    status = forms.MultipleChoiceField(
        choices=SoftwareStatusChoices,
        required=False,
        label=_('Status')
    )

    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        null_option='None',   
        label=_('Manufacturer')
    )

    tag = TagFilterField(model)

    
class SoftwareCSVForm(NetBoxModelImportForm):

    status = CSVChoiceField(
        choices=SoftwareStatusChoices,
        help_text=_('Status'),
        required=True,
    )
    
    manufacturer = CSVModelChoiceField(
        label=_("Manufacturer"),
        queryset=Manufacturer.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Assigned manufacturer')
    )
    
    class Meta:
        model = Software
        fields = ['name' ,'status', 'url', 'manufacturer', 'description', 'tags']
        default_return_url = 'plugins:adestis_netbox_applications:Software_list'


    