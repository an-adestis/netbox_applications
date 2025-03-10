from django.db import models as django_models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *
from dcim.models import *
from virtualization.models import *

__all__ = (
    'InstalledApplicationStatusChoices',
    'InstalledApplication',
)

class InstalledApplicationStatusChoices(ChoiceSet):
    key = 'InstalledApplications.status'

    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_INACTIVE, 'Inactive', 'red'),
    ]
    
class InstalledApplication(NetBoxModel):

    status = django_models.CharField(
        max_length=50,
        choices=InstalledApplicationStatusChoices,
        verbose_name='Status',
        help_text='Status'
    )

    comments = django_models.TextField(
        blank=True
    )
    
    name = django_models.CharField(
        max_length=150
    )
    
    description = django_models.CharField(
        max_length=500,
        blank = True
    )
    
    url = django_models.URLField(
        max_length=2048,
        verbose_name='URL',
        blank=True
    )
    
    version = django_models.CharField(
         max_length=200,
     )
    
    virtual_machine = django_models.ForeignKey(
          to='virtualization.VirtualMachine',
          on_delete = django_models.PROTECT,
          related_name= 'applications_virtual_machine',
          null=True,
          verbose_name='Virtual Machine'
    )
    
    device = django_models.ForeignKey(
        to = 'dcim.Device',
        on_delete = django_models.PROTECT,
        related_name= 'applications_device',
        null = True,
        verbose_name='Device'
    )
    
    tenant = django_models.ForeignKey(
         to = 'tenancy.Tenant',
         on_delete = django_models.PROTECT,
         related_name = 'applications_tenant',
         null = True,
         verbose_name='Tenant'
     )
    
    tenant_group = django_models.ForeignKey(
        to= 'tenancy.TenantGroup',
        on_delete= django_models.PROTECT,
        related_name='applications_tenant_group',
        null = True,
        verbose_name= 'Tenant Group'
    )
    
    manufacturer = django_models.ForeignKey(
        to= 'dcim.Manufacturer',
        on_delete= django_models.PROTECT,
        related_name= 'applications_manufacturer',
        null= True,
        verbose_name='Manufacturer'
    )
    
    cluster = django_models.ForeignKey(
        to = 'virtualization.Cluster',
        on_delete = django_models.PROTECT,
        related_name = 'applications_cluster',
        null = True,
        verbose_name='Cluster'
    )
    
    cluster_group = django_models.ForeignKey(
        to = 'virtualization.ClusterGroup',
        on_delete = django_models.PROTECT,
        related_name = 'applications_cluster_group',
        null = True,
        verbose_name='Cluster Group'
    )
    
    class Meta:
        verbose_name_plural = "Applications"
        verbose_name = 'Application'

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_applications:installedapplication', args=[self.pk])

    def get_status_color(self):
        return InstalledApplicationStatusChoices.colors.get(self.status)
    
    def __str__(self):
        return self.name 