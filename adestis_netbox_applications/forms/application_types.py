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

    fieldsets = (
        FieldSet('name', 'comment', 'tags',   name=_('Application Types')),
    )

    class Meta:
        model = InstalledApplicationTypes
        fields = ['name', 'comment', 'tags']
        
    
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
    
    
    comment = forms.CharField(
        max_length=500,
        required=False,
        label=_("Comment"),
    )
    
    model = InstalledApplicationTypes

    fieldsets = (
        FieldSet('name', 'comment', 'tags',  name=_('Application Types')),
    )

    nullable_fields = [
         'add_tags', 'remove_tags', 'comment', ''
    ]
    
class InstalledApplicationTypesFilterForm(NetBoxModelFilterSetForm):
    
    model = InstalledApplicationTypes

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'comment', 'tag',  name=_('Application Types')),
    )

    index = forms.IntegerField(
        required=False
    )

    tag = TagFilterField(model)

    
class InstalledApplicationTypesCSVForm(NetBoxModelImportForm):

    class Meta:
        model = InstalledApplicationTypes
        fields = ['name', 'comment', 'tags']
        default_return_url = 'plugins:adestis_netbox_applications:InstalledApplicationTypes_list'


    