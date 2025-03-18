from django.db import models as django_models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
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
    
    url = django_models.URLField(
        max_length=300
    )
    
    virtual_machine = django_models.ManyToManyField(
        to='virtualization.VirtualMachine',
        through='ApplicationVirtualMachine',
        verbose_name='Virtual Machines'
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
    
    device = django_models.ManyToManyField(
        to = 'dcim.Device',
        through='ApplicationDevice',
        verbose_name='Device'
    )
    
    cluster = django_models.ManyToManyField(
        to = 'virtualization.Cluster',
        through='ApplicationCluster',
        verbose_name='Cluster'
    )
    
    cluster_group = django_models.ManyToManyField(
        to = 'virtualization.ClusterGroup',
        through= 'ApplicationClusterGroup',
        verbose_name='Cluster Group'
    )
    
    software = django_models.ForeignKey(
        to='adestis_netbox_applications.Software',
        on_delete=django_models.PROTECT,
        related_name='applications_software',
        null=True,
        verbose_name='Software'
    )
    
    class ApplicationVirtualMachine(django_models.Model):
     application = django_models.ForeignKey(
        'InstalledApplication',
        on_delete=django_models.CASCADE,
        related_name='applications_virtual_machines',
        verbose_name='Installed Application'
    )
    virtual_machine = django_models.ForeignKey(
        'virtualization.VirtualMachine',
        on_delete=django_models.PROTECT,
        related_name='applications_virtual_machines',
        verbose_name='Virtual Machine',
        null=True
    )
    class ApplicationDevice(django_models.Model):
     application = django_models.ForeignKey(
        'InstalledApplication',
        on_delete=django_models.CASCADE,
        related_name='applications_device',
        verbose_name='Installed Application'
    )
    
    device = django_models.ForeignKey(
        'dcim.Device',
        on_delete=django_models.PROTECT,
        related_name= 'applications_device',
        null = True,
        verbose_name='Device'
    )
    
    class ApplicationCluster(django_models.Model):
     application = django_models.ForeignKey(
        'InstalledApplication',
        on_delete=django_models.CASCADE,
        related_name='applications_cluster',
        verbose_name='Installed Application'
    ) 
     
    cluster = django_models.ForeignKey(
         'virtualization.Cluster',
         on_delete=django_models.PROTECT,
         null = True,
         verbose_name='Cluster',
         related_name='applications_cluster'
     )
    
    class ApplicationClusterGroup(django_models.Model):
     application = django_models.ForeignKey(
        'InstalledApplication',
        on_delete=django_models.CASCADE,
        related_name='applications_cluster_group',
        verbose_name='Installed Application'
    ) 
    cluster_group = django_models.ForeignKey(
         'virtualization.ClusterGroup',
         on_delete=django_models.PROTECT,
         verbose_name='Cluster Group',
         null = True,
         related_name='applications_cluster_group'
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