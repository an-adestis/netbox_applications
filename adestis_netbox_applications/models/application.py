from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *

__all__ = (
    'ApplicationStatusChoices',
    'Application',
)

class ApplicationStatusChoices(ChoiceSet):
    key = 'Applications.status'

    # TODO: Add status states
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'


    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_INACTIVE, 'Inactive', 'red'),
    ]
    
class Application(NetBoxModel):


    # TODO: Add fields to store the application data

    status = models.CharField(
        max_length=50,
        choices=ApplicationStatusChoices,
        verbose_name='Status',
        help_text='Status'
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name_plural = "Applications"
        verbose_name = 'Applications'
        # TODO: Add constraints to ensure that a unique application will not be stored twice            
        # ordering = ('contact',)
        # constraints = [
        # ]

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_applications:application', args=[self.pk])

    def get_status_color(self):
        return ApplicationStatusChoices.colors.get(self.status)
