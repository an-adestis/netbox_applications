from django.db import models as django_models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *
from dcim.models import *
from virtualization.models import *

__all__ = (
    'SoftwareStatusChoices',
    'SoftwareApprovalStatusChoises',
    'Software',
)

class SoftwareApprovalStatusChoises(ChoiceSet):
    key = 'Software.approval_status'
    
    NEEDS_APPROVAL = 'needs_approval'
    ALL_VERSION_APPROVED = 'all_versions_approved'
    VERSION_CHANGED = 'version_changed'
    NOT_APPROVAL = 'not_approved'
    
    CHOICES = [
        (NEEDS_APPROVAL, 'Needs Approval', 'yellow'),
        (ALL_VERSION_APPROVED, 'All Versions Approved', 'green'),
        (VERSION_CHANGED, 'Version changed - needs Approval', 'cyan'),
        (NOT_APPROVAL, 'Not Approved', 'red'),
    ]

class SoftwareStatusChoices(ChoiceSet):
    key = 'Software.status'

    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_PLANNED ='planned'
    STATUS_DECOMISSIONING = 'decomissioning'
    STATUS_REMOVED = 'removed'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_INACTIVE, 'Inactive', 'red'),
        (STATUS_PLANNED, 'Planned', 'blue'),
        (STATUS_DECOMISSIONING, 'Decomissioning', 'orange'),
        (STATUS_REMOVED, 'Removed', 'gray'),
    ]
    
class Software(NetBoxModel):

    status = django_models.CharField(
        max_length=50,
        choices=SoftwareStatusChoices,
        verbose_name='Status',
        help_text='Status'
    )
    
    name = django_models.CharField(
        max_length=150
    )
    
    approval_status = django_models.CharField(
        choises = SoftwareApprovalStatusChoises,
        verbose_name = 'Approval Status',
        help_text = 'Approval Status'
    )
    
    parent_software = django_models.ForeignKey(
        'self',
        verbose_name='Parent Software',
        on_delete = django_models.CASCADE,
        null=True,
        blank=True,
        related_name='parent_software'
    )
    
    approval_info = django_models.TextField(
        blank=True
    )
    
    description = django_models.CharField(
        max_length=500,
        blank = True
    )
    
    url = django_models.URLField(
        max_length=300
    )
    
    manufacturer = django_models.ForeignKey(
        to= 'dcim.Manufacturer',
        on_delete= django_models.PROTECT,
        related_name= 'software_manufacturer',
        null= True,
        verbose_name='Manufacturer'
    )
    
    contact_group = django_models.ForeignKey(
        to = 'tenancy.ContactGroup',
        on_delete = django_models.PROTECT,
        related_name='software_contact_group',
        verbose_name='Contact Group',
        blank = True,
        null = True,
    )
    
    contact = django_models.ManyToManyField(
        to='tenancy.Contact',
        related_name='software_contact',
        blank = True,
        verbose_name='Contact',
        help_text='Contact that uses the Application'
    )
    
    class Meta:
        verbose_name_plural = "Software"
        verbose_name = 'Software'
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_applications:software', args=[self.pk])

    def get_status_color(self):
        return SoftwareStatusChoices.colors.get(self.status)
        return SoftwareApprovalStatusChoises.color.get(self.approval_status) 
    
    def __str__(self):
        return self.name 