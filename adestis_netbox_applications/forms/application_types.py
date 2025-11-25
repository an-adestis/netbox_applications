from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_applications.models import *
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    TagFilterField,
    CSVModelChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    SlugField,
)
from utilities.forms.widgets import DatePicker
from dcim.models import *
from virtualization.models import *


__all__ = (
    'InstalledApplicationTypesForm',
    'InstalledApplicationTypesFilterForm',
    'InstalledApplicationTypesBulkEditForm',
    'InstalledApplicationTypesCSVForm',
)

class InstalledApplicationTypesForm(NetBoxModelForm):

    slug = SlugField()
    
    fieldsets = (
        FieldSet('name', 'slug', 'tags', name=_('Application Types')),
    )

    class Meta:
        model = InstalledApplicationTypes
        fields = ['name', 'slug', 'tags']
        
    
class InstalledApplicationTypesBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Software.objects.all(),
        widget=forms.MultipleHiddenInput, 
    )
    
    name = forms.CharField(
        required=False,
        max_length = 150,
        label=_("Name"),
    )
    
    slug = SlugField()
    
    model = InstalledApplicationTypes

    fieldsets = (
        FieldSet('name', 'slug',  'tags',  name=_('Application Types')),
    )

    nullable_fields = [
         'add_tags', 'remove_tags'
    ]
    
class InstalledApplicationTypesFilterForm(NetBoxModelFilterSetForm):
    
    model = InstalledApplicationTypes

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'slug', 'tag',  name=_('Application Types')),
    )

    index = forms.IntegerField(
        required=False
    )

    tag = TagFilterField(model)

    
class InstalledApplicationTypesCSVForm(NetBoxModelImportForm):

    class Meta:
        model = InstalledApplicationTypes
        fields = ['name', 'slug', 'tags']
        default_return_url = 'plugins:adestis_netbox_applications:InstalledApplicationTypes_list'


    