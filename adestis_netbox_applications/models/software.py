from django.db import models as django_models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *
from dcim.models import *
from virtualization.models import *

__all__ = (
    'SoftwareStatusChoices',
    'Software',
)

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
        related_name= 'applications_manufacturer',
        null= True,
        verbose_name='Manufacturer'
    )
    
    class Meta:
        verbose_name_plural = "Softwares"
        verbose_name = 'Software'

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_applications:software', args=[self.pk])

    def get_status_color(self):
        return SoftwareStatusChoices.colors.get(self.status)
    
    def __str__(self):
        return self.name 