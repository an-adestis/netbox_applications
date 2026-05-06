from django.db import models as django_models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *
from dcim.models import *
from virtualization.models import *
from adestis_netbox_applications.models.software import *

__all__ = (
    'SoftwareVersion',
)

class SoftwareVersionApprovalStatusChoices(ChoiceSet):
    key = 'Software.approval_status'
    
    NEEDS_APPROVAL = 'needs_approval'
    VERSION_APPROVED = 'version_approved'
    INSTANCE_APPROVAL = 'version_approved_instance_approval_required'
    NOT_APPROVAL = 'not_approved'
    
    CHOICES = [
        (NEEDS_APPROVAL, 'Needs Approval', 'yellow'),
        (VERSION_APPROVED, 'Version Approved', 'green'),
        (INSTANCE_APPROVAL, 'Version Approved - Instance Approval required', 'blue'),
        (NOT_APPROVAL, 'Not Approved', 'red'),
    ]
    
class SoftwareVersion(NetBoxModel):
    
    name = django_models.CharField(
        max_length=150
    )
    
    approval_status = django_models.CharField(
        max_length=50,
        choices=SoftwareVersionApprovalStatusChoices,
        verbose_name = 'Approval Status',
        help_text = 'Approval Status',
        null=True
    )
    
    software = django_models.ForeignKey(
        to='adestis_netbox_applications.Software',
        verbose_name='Software',
        on_delete = django_models.CASCADE,
        null=True,
        related_name='related_software'
    )
    
    approval_info = django_models.TextField(
        blank=True
    )
    
    description = django_models.CharField(
        max_length=500,
        blank = True
    )
    
    version = django_models.CharField(
        max_length=150,
        blank=True
    )
    
    class Meta:
        verbose_name_plural = "Software Versions"
        verbose_name = 'Software Version'
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_applications:softwareversion', args=[self.pk])

    def get_approval_status_color(self):
        return SoftwareVersionApprovalStatusChoices.colors.get(self.approval_status) 

    def __str__(self):
        return self.name 