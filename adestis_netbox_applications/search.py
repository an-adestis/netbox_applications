from netbox.search import SearchIndex, register_search
from .models.application import InstalledApplication
from .models.software import Software
from .models.software_version import SoftwareVersion
from .models.application_types import InstalledApplicationTypes


@register_search
class InstalledApplicationIndex(SearchIndex):
    model = InstalledApplication
    fields = (
        ('name', 100),
        ('status', 1000),
        ('version', 1000),
        ('description', 500),
        ('comments', 2000),
        ('url', 1000),
        ('approval_info', 2000),
    )


@register_search
class SoftwareIndex(SearchIndex):
    model = Software
    fields = (
        ('name', 100),
        ('status', 1000),
        ('description', 500),
        ('url', 1000),
    )


@register_search
class SoftwareVersionIndex(SearchIndex):
    model = SoftwareVersion
    fields = (
        ('name', 100),
        ('version', 500),
        ('description', 1000),
        ('approval_status', 1000),
        ('approval_info', 2000),
    )


@register_search
class InstalledApplicationTypesIndex(SearchIndex):
    model = InstalledApplicationTypes
    fields = (
        ('name', 100),
        ('slug', 1000),
    )