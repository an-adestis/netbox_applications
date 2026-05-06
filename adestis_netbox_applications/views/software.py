from netbox.views import generic
from adestis_netbox_applications.forms.software import *
from adestis_netbox_applications.models.software import *
from adestis_netbox_applications.filtersets.software import *
from adestis_netbox_applications.tables.software import *
from netbox.views import generic
from django.utils.translation import gettext as _
from utilities.views import GetRelatedModelsMixin, ViewTab, register_model_view
from tenancy.models import *
from tenancy.forms import *
from tenancy.filtersets import *
from tenancy.tables import *
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db import transaction
from django.contrib import messages

from django.db import models as django_models

__all__ = (
    'SoftwareView',
    'SoftwareListView',
    'SoftwareEditView',
    'SoftwareDeleteView',
    'SoftwareBulkDeleteView',
    'SoftwareBulkEditView',
    'SoftwareBulkImportView',
    
    'SoftwareAffectedSuccessorSoftwareView',
    
    'SoftwareAffectedContactView',
    'ContactAffectedSoftwareView',
    'SoftwareAssignContact',
    'SoftwareRemoveContactView',
)

@register_model_view(Software)
class SoftwareView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = Software.objects.all()
    
    def get_extra_context(self, request, instance):
        software_versions = instance.related_software.restrict(request.user, 'view').all()
        return {
            'related_models': self.get_related_models(request, instance),
            'software_versions': software_versions,
        }

class SoftwareListView(generic.ObjectListView):
    queryset = Software.objects.all()
    table = SoftwareTable
    filterset = SoftwareFilterSet
    filterset_form = SoftwareFilterForm
    template_name = 'adestis_netbox_applications/software_list.html'
    
    def get_queryset(self, request):
        qs = Software.objects.restrict(request.user, 'view')
        
        def sort_hierarchical(apps, parent=None, result=None):
            if result is None:
                result = []
            for app in apps:
                if app.parent_software == parent:
                    result.append(app)
                    sort_hierarchical(apps, parent=app, result=result)
            return result

        all_apps = list(qs)
        sorted_apps = sort_hierarchical(all_apps)
        pks_ordered = [app.pk for app in sorted_apps]
        
        preserved = django_models.Case(
            *[django_models.When(pk=pk, then=pos) for pos, pk in enumerate(pks_ordered)]
        )
        return qs.filter(pk__in=pks_ordered).order_by(preserved)
    

class SoftwareEditView(generic.ObjectEditView):
    queryset = Software.objects.all()
    form = SoftwareForm


class SoftwareDeleteView(generic.ObjectDeleteView):
    queryset = Software.objects.all() 

class SoftwareBulkDeleteView(generic.BulkDeleteView):
    queryset = Software.objects.all()
    table = SoftwareTable
    
    
class SoftwareBulkEditView(generic.BulkEditView):
    queryset = Software.objects.all()
    filterset = SoftwareFilterSet
    table = SoftwareTable
    form =  SoftwareBulkEditForm
    

class SoftwareBulkImportView(generic.BulkImportView):
    queryset = Software.objects.all()
    model_form = SoftwareCSVForm
    table = SoftwareTable
    
@register_model_view(Software, name='successor_software')
class SoftwareAffectedSuccessorSoftwareView(generic.ObjectChildrenView):
    queryset = Software.objects.all()
    child_model= Software
    table = SoftwareTable
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
    }

    tab = ViewTab(
        label=_('Successor Software'),
        badge=lambda obj: Software.objects.filter(parent_software=obj).count(),
        hide_if_empty=False,
        weight=600
    )
    
    def get_children(self, request, parent):
        def get_descendants(app):
            children = Software.objects.restrict(request.user, 'view').filter(
                parent_software=app
            )
            result = list(children)
            for child in children:
                result.extend(get_descendants(child))
            return result

        descendants = get_descendants(parent)
        pks = [obj.pk for obj in descendants]
        qs = Software.objects.restrict(request.user, 'view').filter(pk__in=pks)
        self.tab.badge = lambda obj: qs.count()
        return qs
    
@register_model_view(Software, name='contacts')
class SoftwareAffectedContactView(generic.ObjectChildrenView):
    queryset = Software.objects.all()
    child_model= Contact
    table = ContactTableSoftware
    template_name = "adestis_netbox_applications/software_contact.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_contact': {'change'},
    }

    tab = ViewTab(
        label=_('Contacts'),
        badge=lambda obj: obj.contact.count(),
        weight=600
    )

    def get_children(self, request, parent):
        return Contact.objects.restrict(request.user, 'view').filter(software_contact=parent)
        
@register_model_view(Contact, name='software_contact')
class ContactAffectedSoftwareView(generic.ObjectChildrenView):
    queryset = Contact.objects.all()
    child_model= Software
    table = SoftwareTable
    template_name = "adestis_netbox_applications/contact_software.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_software': {'change'},
    }

    tab = ViewTab(
        label=_('Software'),
        badge=lambda obj: obj.software_contact.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return Software.objects.restrict(request.user, 'view').filter(contact=parent)
    
@register_model_view(Software, 'assign_contact')
class SoftwareAssignContact(generic.ObjectEditView):
    queryset = Software.objects.prefetch_related(
        'contact', 'tags', 
    ).all()
    
    form = SoftwareAssignContactForm
    template_name = 'adestis_netbox_applications/assign_software_contact.html'

    def get(self, request, pk):
        software = get_object_or_404(self.queryset, pk=pk)
        form = self.form(software, initial=request.GET)

        return render(request, self.template_name, {
            'software': software,
            'form': form,
            'return_url': reverse('plugins:adestis_netbox_applications:software', kwargs={'pk': pk}),
            'edit_url': reverse('plugins:adestis_netbox_applications:software_assign_contact', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        software = get_object_or_404(self.queryset, pk=pk)
        form = self.form(software, request.POST)

        if form.is_valid():
            
            selected_contact_groups = form.cleaned_data['contact_group']
            selected_contacts = form.cleaned_data['contact']
            with transaction.atomic():
                
                for contact in Contact.objects.filter(pk__in=selected_contacts): 
                    software.contact.add(contact)
                    
                for contact_group in ContactGroup.objects.filter(pk__in=selected_contact_groups): 
                    software.contact_group.add(contact_group)
            
            software.save()
            
            return redirect(software.get_absolute_url())

        return render(request, self.template_name, {
            'software': software,
            'form': form,
            'return_url': software.get_absolute_url(),
            'edit_url': reverse('plugins:adestis_netbox_applications:software_assign_contact', kwargs={'pk': pk}),
        })
        
@register_model_view(Software, 'remove_contact', path='contact/remove')
class SoftwareRemoveContactView(generic.ObjectEditView):
    queryset = Software.objects.all()
    form = SoftwareRemoveContact
    template_name = 'generic/bulk_remove.html'

    def post(self, request, pk):

        software = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            
            form = self.form(request.POST)
            if form.is_valid():
                
                contact_pks = form.cleaned_data['pk']
                with transaction.atomic():
                    software.contact.remove(*contact_pks)
                    software.save()

                messages.success(request, _("Removed {count} contact from installedapplication {software}").format(
                    count=len(contact_pks),
                    software=software
                ))
                return redirect(software.get_absolute_url())
        else:
            form = self.form(initial={'pk': request.POST.getlist('pk')})

        selected_objects = Contact.objects.filter(pk__in=form.initial['pk'])
        contact_table = ContactTable(list(selected_objects), orderable=False)
        contact_table.configure(request)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': software,
            'table': contact_table,
            'obj_type_plural': 'contacts',
            'return_url': software.get_absolute_url(),
        })
    