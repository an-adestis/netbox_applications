from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_applications.models.software_version import SoftwareVersion, SoftwareVersionApprovalStatusChoices
from adestis_netbox_applications.models.software import Software
from adestis_netbox_applications.models.application import InstalledApplication
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    TagFilterField,
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from utilities.forms import ConfirmationForm

__all__ = (
    'SoftwareVersionForm',
    'SoftwareVersionFilterForm',
    'SoftwareVersionBulkEditForm',
    'SoftwareVersionCSVForm',

)

class SoftwareVersionForm(NetBoxModelForm):
    
    software = DynamicModelChoiceField(
        queryset=Software.objects.all(),
        required=True,
        help_text=_("Software"),
    )
    
    version = forms.CharField(
        required=True,
        
    )

    fieldsets = (
        FieldSet('name', 'version', 'software', 'description', 'tags',  name=_('Software Version')),
        FieldSet('approval_status', 'approval_info', name=_('Software Approval')),
    )

    class Meta:
        model = SoftwareVersion
        fields = ['name', 'description', 'tags', 'version', 'software', 'approval_status', 'approval_info',]

class SoftwareVersionBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=SoftwareVersion.objects.all(),
        widget=forms.MultipleHiddenInput, 
    )
    
    name = forms.CharField(
        required=False,
        max_length = 150,
        label=_("Name"),
    )
    
    version = forms.CharField(
        required=False,
        max_length= 150,
        label=_("Version")
    )
    
    description = forms.CharField(
        max_length=500,
        required=False,
        label=_("Description"),
    )
    
    approval_info = forms.CharField(
        max_length=150,
        required=False,
        label=_("Approval Information")
    )
    
    approval_status = forms.ChoiceField(
        required=False,
        choices=SoftwareVersionApprovalStatusChoices,
    )
    
    software = DynamicModelChoiceField(
        label=_('Assigned Software'),
        queryset=Software.objects.all(),
        required = True,
    )
    
    model = SoftwareVersion

    fieldsets = (
        FieldSet('name', 'version', 'software', 'description', 'tags',  name=_('Software Version')),
        FieldSet('approval_status', 'approval_info', name=_('Software Approval')),
    )

    nullable_fields = [
        'add_tags', 'remove_tags', 'description', 'name', 'version', 'approval_info', 'approval_status'
    ]
    
class SoftwareVersionFilterForm(NetBoxModelFilterSetForm):
    
    model = SoftwareVersion

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'tag', 'version', 'software_id', name=_('Software Version')),
        FieldSet('approval_status', 'approval_info', name=_('Software Approval')),
    )

    index = forms.IntegerField(
        required=False
    )
    
    approval_status = forms.MultipleChoiceField(
        choices=SoftwareVersionApprovalStatusChoices,
        required=False,
        label=_('Approval Status')
    )
    
    software_id = DynamicModelMultipleChoiceField(
        label=_('Assiged Software'),
        queryset=Software.objects.all(),
        required = True,
    )
    
    installedapplication_id = DynamicModelMultipleChoiceField(
        label=_('Assiged Application'),
        queryset=InstalledApplication.objects.all(),
        required = True,
    )
    
    tag = TagFilterField(model)

class SoftwareVersionCSVForm(NetBoxModelImportForm):

    approval_status = CSVChoiceField(
        choices=SoftwareVersionApprovalStatusChoices,
        help_text=_('Status'),
        required=True,
    )
    
    software = CSVModelChoiceField(
        label=_("Software"),
        queryset=Software.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned Software')
    )

    class Meta:
        model = SoftwareVersion
        fields = ['name', 'software', 'version', 'approval_status', 'approval_info', 'description', 'tags',   ]
        default_return_url = 'plugins:adestis_netbox_applications:SoftwareVersion_list'
        
