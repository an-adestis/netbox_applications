from django.db import models as django_models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *
from dcim.models import *
from virtualization.models import *

__all__ = (
    'InstalledApplicationTypes',
)
    
class InstalledApplicationTypes(NetBoxModel):

    name = django_models.CharField(
        max_length=150
    )
    
    comment = django_models.CharField(
        max_length=500,
        blank = True
    )
    
    class Meta:
        verbose_name_plural = "Application Type"
        verbose_name = 'Application Types'

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_applications:installedapplicationtypes', args=[self.pk])

    def __str__(self):
        return self.name 