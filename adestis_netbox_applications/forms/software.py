from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_applications.models.software import Software, SoftwareStatusChoices, SoftwareApprovalStatusChoices
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
from utilities.forms.widgets import DatePicker
from dcim.models import *
from virtualization.models import *
from tenancy.models import Contact, ContactGroup

__all__ = (
    'SoftwareForm',
    'SoftwareFilterForm',
    'SoftwareBulkEditForm',
    'SoftwareCSVForm',
    'SoftwareAssignContactForm',
    'SoftwareRemoveContact',
)

class SoftwareForm(NetBoxModelForm):
    
    parent_software = DynamicModelMultipleChoiceField(
        queryset=Software.objects.all(),
        required=False,
        help_text=_("Parent Software"),
    )
    
    contact = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        query_params={
            'group_id': '$contact_group',
        },
        help_text=_("Contacts"),
    )
    
    contact_group = DynamicModelChoiceField(
        queryset=ContactGroup.objects.all(),
        required = False,
        label = ("Contact Group")
    )

    fieldsets = (
        FieldSet('name', 'description', 'url', 'tags', 'status', 'manufacturer', name=_('Software')),
        FieldSet('parent_software', 'approval_status', 'approval_info', name=_('Software Approvement')),
        FieldSet('contact', 'contact_group', name=('Contact')),
    )

    class Meta:
        model = Software
        fields = ['name', 'description', 'url', 'tags', 'status', 'manufacturer', 'parent_software', 'approval_status', 'approval_info', 'contact_group', 'contact']
        
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
    
    contact = DynamicModelMultipleChoiceField(
        label=_('Contacts'),
        queryset=Contact.objects.all(),
        required = False,
        query_params={
            'group_id': '$contact_group',
        },
    )
    
    contact_group = DynamicModelChoiceField(
        queryset=ContactGroup.objects.all(),
        required = False,
        label = ("Contact Group")
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
    
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        null_option='None',   
        label=_('Manufacturer')
    )
    
    approval_status = forms.ChoiceField(
        required=False,
        choices=SoftwareApprovalStatusChoices,
    )
    
    parent_software = DynamicModelMultipleChoiceField(
        label=_('Parent Software'),
        queryset=Software.objects.all(),
        required = False,
    )
    
    model = Software

    fieldsets = (
        FieldSet('name', 'description', 'url', 'tags', 'status', 'manufacturer', name=_('Software')),
        FieldSet('parent_software', 'approval_status', 'approval_info', name=_('Software Approvement')),
        FieldSet('contact', 'contact_group', name=('Contact')),
    )

    nullable_fields = [
         'add_tags', 'remove_tags', 'description', ''
    ]
    
class SoftwareFilterForm(NetBoxModelFilterSetForm):
    
    model = Software

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'url', 'tag', 'status', 'manufacturer_id',  name=_('Software')),
        FieldSet('parent_software_id', 'approval_status', 'approval_info', name=_('Software Approvement')),
        FieldSet('contact', 'contact_group_id', name=_('Contact'))
    )

    index = forms.IntegerField(
        required=False
    )

    status = forms.MultipleChoiceField(
        choices=SoftwareStatusChoices,
        required=False,
        label=_('Status')
    )
    
    approval_status = forms.MultipleChoiceField(
        choices=SoftwareApprovalStatusChoices,
        required=False,
        label=_('Approval Status')
    )
    
    parent_software_id = DynamicModelMultipleChoiceField(
        label=_('Parent Software'),
        queryset=Software.objects.all(),
        required = False,
    )

    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        null_option='None',   
        label=_('Manufacturer')
    )
    
    contact_group_id = DynamicModelMultipleChoiceField(
        queryset=ContactGroup.objects.all(),
        required=False,
        null_option='None',
        label=_('Contact Group')
    )
    
    contact = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label=_('Contacts')
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
        required=False,
        to_field_name='name',
        help_text=_('Assigned manufacturer')
    )
    
    contact_group = CSVModelChoiceField(
        label=_('Contact Group'),
        queryset=ContactGroup.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Assigned contact_group')
    )
    
    contact = CSVModelMultipleChoiceField(
        label=_('Contacts'),
        queryset=Contact.objects.all(),
        required = True,
        to_field_name='name',
        help_text=_('Assigned contact')
    )
    
    class Meta:
        model = Software
        fields = ['name' ,'status', 'url', 'manufacturer', 'description', 'tags', 'parent_software', 'approval_status', 'approval_info', 'contact_group', 'contact' ]
        default_return_url = 'plugins:adestis_netbox_applications:Software_list'
        
class SoftwareAssignContactForm(forms.Form):
    
    contact = DynamicModelMultipleChoiceField(
        label=_('Contacts'),
        queryset=Contact.objects.all()
    )

    class Meta:
        fields = [
            'contact',
        ]

    def __init__(self, certificate, *args, **kwargs):

        self.certificate = certificate

        self.contact = DynamicModelMultipleChoiceField(
            label=_('Contacts'),
            queryset=Contact.objects.all()
        )        

        super().__init__(*args, **kwargs)

        self.fields['contact'].choices = []  
        
class SoftwareRemoveContact(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        widget=forms.MultipleHiddenInput()
    )