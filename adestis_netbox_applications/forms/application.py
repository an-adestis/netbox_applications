from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_applications.models.application import Application, ApplicationStatusChoices
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet

__all__ = (
    'ApplicationForm',
    'ApplicationFilterForm',
    'ApplicationBulkEditForm',
    'ApplicationCSVForm',
)

class ApplicationForm(NetBoxModelForm):
    comments = CommentField()


    fieldsets = (
        FieldSet('status', 'tags'),
    )

    class Meta:
        model = Application
        fields = ['status', 'comments', 'tags']
        help_texts = {
            'status': "Example text",
        }


class ApplicationBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Application.objects.all(),
        widget=forms.MultipleHiddenInput
    )

    status = forms.ChoiceField(
        required=False,
        choices=ApplicationStatusChoices,
    )

    model = Application

    fieldsets = (
        FieldSet('status'),
    )

    nullable_fields = [
         'add_tags', 'remove_tags'
    ]


class ApplicationFilterForm(NetBoxModelFilterSetForm):
    
    model = Application

    fieldsets = (
        FieldSet('q', 'index', 'tag'),
        FieldSet('status'),
    )

    index = forms.IntegerField(
        required=False
    )

    status = forms.MultipleChoiceField(
        choices=ApplicationStatusChoices,
        required=False,
        label=_('Status')
    )

    tag = TagFilterField(model)


class ApplicationCSVForm(NetBoxModelImportForm):

    status = CSVChoiceField(
        choices=ApplicationStatusChoices,
        help_text=_('Status'),
        required=True,
    )

    class Meta:
        model = Application
        fields = ['status']
        default_return_url = 'plugins:adestis_netbox_applications:Application_list'
