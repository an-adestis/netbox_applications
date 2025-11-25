from django.db import models as django_models
from adestis_netbox_applications.models.application import *
from netbox.models import OrganizationalModel
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *
from dcim.models import *
from virtualization.models import *

__all__ = (
    'InstalledApplicationTypes',
)
    
class InstalledApplicationTypes(OrganizationalModel):

    name = django_models.CharField(
        max_length=150
    )
    
    slug = django_models.SlugField(
        verbose_name='Slug',
        max_length=100,
        unique=True
    )
    
    installedapplication = django_models.ForeignKey(
        to='adestis_netbox_applications.InstalledApplication',
        on_delete= django_models.PROTECT,
        related_name='installed_app',
        null=True,
        verbose_name='Application'
    )
    
    class Meta:
        verbose_name_plural = "Application Type"
        verbose_name = 'Application Types'
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_applications:installedapplicationtypes', args=[self.pk])

    def __str__(self):
        return self.name 