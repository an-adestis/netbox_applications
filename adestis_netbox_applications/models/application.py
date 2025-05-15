from django.db import models as django_models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from tenancy.models import *
from dcim.models import *
from virtualization.models import *
from adestis_netbox_applications.models.software import *

__all__ = (
    'InstalledApplicationStatusChoices',
    'InstalledApplication',
)

class InstalledApplicationStatusChoices(ChoiceSet):
    key = 'InstalledApplications.status'

    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_PLANNED ='planned'
    STATUS_DECOMISSIONING = 'decomissioning'
    STATUS_REMOVED = 'removed'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_INACTIVE, 'Inactive', 'red'),
        (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_DECOMISSIONING, 'Decomissioning', 'yellow'),
        (STATUS_REMOVED, 'Removed', 'gray'),
    ]
    
class InstalledApplication(NetBoxModel):

    status = django_models.CharField(
        max_length=50,
        choices=InstalledApplicationStatusChoices,
        verbose_name='Status',
        help_text='Status'
    )
    
    status_date = django_models.DateField(
        verbose_name='Status Date',
        null=True,
        help_text='Status Date'
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
    
    version = django_models.CharField(
         max_length=200,
    )
    
    url = django_models.URLField(
        max_length=300
    )
    
    device = django_models.ManyToManyField(
        to='dcim.Device',
        verbose_name='Devices',
        through='DeviceAssignment',
        related_name='installedapplication'
    )
    
    cluster = django_models.ManyToManyField(
        to='virtualization.Cluster',
        verbose_name='Clusters',
        through='ClusterAssignment',
        related_name='installedapplication'
    )
    
    cluster_group = django_models.ManyToManyField(
        to='virtualization.ClusterGroup',
        verbose_name='Cluster Groups',
        through='ClusterGroupAssignment',
        related_name='installedapplication'
    )
    
    virtual_machine = django_models.ManyToManyField(
        to='virtualization.VirtualMachine',
        verbose_name='Virtual Machines',
        through='VirtualMachineAssignment',
        related_name='installedapplication'
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
    
    software = django_models.ForeignKey(
        to='adestis_netbox_applications.Software',
        on_delete= django_models.PROTECT,
        related_name= 'applications_software',
        null=True,
        verbose_name='Software'
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
    
class DeviceAssignment(NetBoxModel):
    
    device = django_models.ForeignKey(
        to='dcim.Device',
        on_delete=django_models.PROTECT,
        related_name="device_assignments",
        verbose_name="Device"
    )
    
    installed_application = django_models.ForeignKey('InstalledApplication', on_delete=django_models.CASCADE)
        
class ClusterAssignment(NetBoxModel):
    
    cluster = django_models.ForeignKey(
        to='virtualization.Cluster',
        on_delete=django_models.PROTECT,
        related_name="cluster_assignments",
        verbose_name="Cluster"
    )
    
    installed_application = django_models.ForeignKey('InstalledApplication', on_delete=django_models.CASCADE)
      
class ClusterGroupAssignment(NetBoxModel):
    
    cluster_group = django_models.ForeignKey(
        to='virtualization.ClusterGroup',
        on_delete=django_models.PROTECT,
        related_name="cluster_group_assignments",
        verbose_name="Cluster Group"
    )
    
    installed_application = django_models.ForeignKey('InstalledApplication', on_delete=django_models.CASCADE)
    
class VirtualMachineAssignment(NetBoxModel):
    
    virtual_machine = django_models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=django_models.PROTECT,
        related_name="virtual_machine_assignments",
        verbose_name="Cluster"
    )
    
    installed_application = django_models.ForeignKey('InstalledApplication', on_delete=django_models.CASCADE)