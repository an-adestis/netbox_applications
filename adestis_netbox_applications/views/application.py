from netbox.views import generic
from adestis_netbox_certificate_management.models import Certificate
from adestis_netbox_certificate_management.tables import CertificateTable
from adestis_netbox_applications.forms.application import *
from adestis_netbox_applications.filtersets.application import *
from adestis_netbox_applications.models.application import InstalledApplication, ClusterAssignment, DeviceAssignment, ClusterGroupAssignment, VirtualMachineAssignment
from adestis_netbox_applications.filtersets import *
from adestis_netbox_applications.tables import *
from netbox.views import generic
from django.db.models import Prefetch
from django.utils.translation import gettext as _
from tenancy.models import *
from dcim.models import *
from dcim.forms import *
from dcim.tables import *
from dcim.filtersets import *
from netbox.constants import DEFAULT_ACTION_PERMISSIONS
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
from utilities.views import GetRelatedModelsMixin, ViewTab, register_model_view
from utilities.views import ViewTab, register_model_view
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from core.models import ObjectType as ContentType
from django.contrib.contenttypes.models import ContentType

__all__ = (
    'InstalledApplicationView',
    'InstalledApplicationListView',
    'InstalledApplicationEditView',
    'InstalledApplicationDeleteView',
    'DeviceAssignmentDeleteView',
    'ClusterAssignmentDeleteView',
    'ClusterGroupAssignmentDeleteView',
    'VirtualMachineAssignmentDeleteView',
    'InstalledApplicationBulkDeleteView',
    'InstalledApplicationBulkEditView',
    'InstalledApplicationBulkImportView',
    'DeviceAffectedInstalledApplicationView',
    'ClusterAffectedInstalledApplicationView',
    'ClusterGroupAffectedInstalledApplicationView',
    'VirtualMachineAffectedInstalledApplicationView',
    'InstalledApplicationAssignDevice',
    'InstalledApplicationAssignCluster',
    'InstalledApplicationAssignClusterGroup',
    'InstalledApplicationAssignVirtualMachine',
    'InstalledApplicationRemoveDeviceView',
    'InstalledApplicationRemoveClusterView',
    'InstalledApplicationRemoveClusterGroupView',
    'InstalledApplicationRemoveVirtualMachineView',
    
    'InstalledApplicationAffectedCertificateView',
    'InstalledApplicationAssignCertificate',
    'InstalledApplicationRemoveCertificateView',
)

class InstalledApplicationView(generic.ObjectView):
    queryset = InstalledApplication.objects.all()
    
class InstalledApplicationListView(generic.ObjectListView):
    queryset = InstalledApplication.objects.all()
    table = InstalledApplicationTable
    filterset = InstalledApplicationFilterSet
    filterset_form = InstalledApplicationFilterForm
    

class InstalledApplicationEditView(generic.ObjectEditView):
    queryset = InstalledApplication.objects.all()
    form = InstalledApplicationForm


class InstalledApplicationDeleteView(generic.ObjectDeleteView):
    queryset = InstalledApplication.objects.all() 

class ClusterAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = ClusterAssignment.objects.all() 
    
class ClusterGroupAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = ClusterGroupAssignment.objects.all() 
    
class DeviceAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = DeviceAssignment.objects.all() 
    
class VirtualMachineAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = VirtualMachineAssignment.objects.all() 

class InstalledApplicationBulkDeleteView(generic.BulkDeleteView):
    queryset = InstalledApplication.objects.all()
    table = InstalledApplicationTable
    
    
class InstalledApplicationBulkEditView(generic.BulkEditView):
    queryset = InstalledApplication.objects.all()
    filterset = InstalledApplicationFilterSet
    table = InstalledApplicationTable
    form =  InstalledApplicationBulkEditForm
    

class InstalledApplicationBulkImportView(generic.BulkImportView):
    queryset = InstalledApplication.objects.all()
    model_form = InstalledApplicationCSVForm
    table = InstalledApplicationTable
    
@register_model_view(InstalledApplication, name='certificate')
class InstalledApplicationAffectedCertificateView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= Certificate
    table = CertificateTable
    template_name = "adestis_netbox_applications/application.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_remove_certificate': {'change'},
    }

    tab = ViewTab(
        label=_('Certificate'),
        badge=lambda obj: obj.certificate.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return Certificate.objects.restrict(request.user, 'view').filter(installedapplication=parent)
    
    
@register_model_view(InstalledApplication, 'assign_certificate')
class InstalledApplicationAssignCertificate(generic.ObjectEditView):
    queryset = InstalledApplication.objects.prefetch_related(
        'certificate', 'tags', 
    ).all()
    
    form = InstalledApplicationAssignCertificateForm
    template_name = 'adestis_netbox_applications/assign_certificate.html'

    def get(self, request, pk):
        installedapplication = get_object_or_404(self.queryset, pk=pk)
        form = self.form(installedapplication,  initial=request.GET)

        return render(request, self.template_name, {
            'installedapplication': installedapplication,
            'form': form,
            'return_url': reverse('plugins:adestis_netbox_applications:installedapplication', kwargs={'pk': pk}),
            'edit_url': reverse('plugins:adestis_netbox_applications:installedapplication_assign_certificate', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        installedapplication = get_object_or_404(self.queryset, pk=pk)
        form = self.form(installedapplication, request.POST)

        if form.is_valid():
            
            selected_certificates = form.cleaned_data['certificate']
            with transaction.atomic():
                
                for certificate in Certificate.objects.filter(pk__in=selected_certificates): 
                    installedapplication.certificate.add(certificate)
            
            installedapplication.save()
            
            return redirect(installedapplication.get_absolute_url())

        return render(request, self.template_name, {
            'installedapplication': installedapplication,
            'form': form,
            'return_url': installedapplication.get_absolute_url(),
            'edit_url': reverse('plugins:adestis_netbox_applications:installedapplication_assign_certificate', kwargs={'pk': pk}),
        })
        
@register_model_view(InstalledApplication, 'remove_certificate', path='certificate/remove')
class InstalledApplicationRemoveCertificateView(generic.ObjectEditView):
    queryset = InstalledApplication.objects.all()
    form = InstalledApplicationRemoveCertificate
    template_name = 'generic/bulk_remove.html'

    def post(self, request, pk):

        installedapplication = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            
            form = self.form(request.POST)
            if form.is_valid():
                
                certificate_pks = form.cleaned_data['pk']
                with transaction.atomic():
                    installedapplication.certificate.remove(*certificate_pks)
                    installedapplication.save()

                messages.success(request, _("Removed {count} certificates from applications {installedapplication}").format(
                    count=len(certificate_pks),
                    installedapplication=installedapplication
                ))
                return redirect(installedapplication.get_absolute_url())
        else:
            form = self.form(initial={'pk': request.POST.getlist('pk')})

        selected_objects = Certificate.objects.filter(pk__in=form.initial['pk'])
        certificate_table = CertificateTable(list(selected_objects), orderable=False)
        certificate_table.configure(request)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': installedapplication,
            'table': certificate_table,
            'obj_type_plural': 'certificates',
            'return_url': installedapplication.get_absolute_url(),
        })
    
@register_model_view(InstalledApplication, name='device')
class DeviceAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= Device
    table = DeviceTableApplication
    template_name = "adestis_netbox_applications/device.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_remove_device': {'change'},
    }

    tab = ViewTab(
        label=_('Devices'),
        badge=lambda obj: obj.device.count(),
        weight=600
    )

    def get_children(self, request, parent):
        return Device.objects.restrict(request.user, 'view').filter(installedapplication=parent)

@register_model_view(Device, name='applications')
class DeviceAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = Device.objects.all()
    child_model= InstalledApplication
    table = InstalledApplicationTableTab
    template_name = "adestis_netbox_applications/application_device.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        # 'bulk_import': {'add'},
        # 'bulk_edit': {'change'},
        'bulk_remove_installedapplication': {'change'},
    }

    tab = ViewTab(
        label=_('Applications'),
        badge=lambda obj: obj.installedapplication.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return InstalledApplication.objects.restrict(request.user, 'view').filter(device=parent)
    
    
@register_model_view(InstalledApplication, 'assign_device')
class InstalledApplicationAssignDevice(generic.ObjectEditView):
    queryset = InstalledApplication.objects.prefetch_related(
        'device', 'tags', 
    ).all()
    
    form = InstalledApplicationAssignDeviceForm
    template_name = 'adestis_netbox_applications/assign_device.html'

    def get(self, request, pk):
        installedapplication = get_object_or_404(self.queryset, pk=pk)
        form = self.form(installedapplication,  initial=request.GET)

        return render(request, self.template_name, {
            'installedapplication': installedapplication,
            'form': form,
            'return_url': reverse('plugins:adestis_netbox_applications:installedapplication', kwargs={'pk': pk}),
            'edit_url': reverse('plugins:adestis_netbox_applications:installedapplication_assign_device', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        installedapplication = get_object_or_404(self.queryset, pk=pk)
        form = self.form(installedapplication, request.POST)

        if form.is_valid():
            
            selected_devices = form.cleaned_data['device']
            with transaction.atomic():
                
                for device in Device.objects.filter(pk__in=selected_devices): 
                    installedapplication.device.add(device)
            
            installedapplication.save()
            
            return redirect(installedapplication.get_absolute_url())

        return render(request, self.template_name, {
            'installedapplication': installedapplication,
            'form': form,
            'return_url': installedapplication.get_absolute_url(),
            'edit_url': reverse('plugins:adestis_netbox_applications:installedapplication_assign_device', kwargs={'pk': pk}),
        })
        
@register_model_view(InstalledApplication, 'remove_device', path='device/remove')
class InstalledApplicationRemoveDeviceView(generic.ObjectEditView):
    queryset = InstalledApplication.objects.all()
    form = InstalledApplicationRemoveDevice
    template_name = 'generic/bulk_remove.html'

    def post(self, request, pk):

        installedapplication = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            
            form = self.form(request.POST)
            if form.is_valid():
                
                device_pks = form.cleaned_data['pk']
                with transaction.atomic():
                    installedapplication.device.remove(*device_pks)
                    installedapplication.save()

                messages.success(request, _("Removed {count} devices from applications {installedapplication}").format(
                    count=len(device_pks),
                    installedapplication=installedapplication
                ))
                return redirect(installedapplication.get_absolute_url())
        else:
            form = self.form(initial={'pk': request.POST.getlist('pk')})

        selected_objects = Device.objects.filter(pk__in=form.initial['pk'])
        device_table = DeviceTable(list(selected_objects), orderable=False)
        device_table.configure(request)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': installedapplication,
            'table': device_table,
            'obj_type_plural': 'devices',
            'return_url': installedapplication.get_absolute_url(),
        })

@register_model_view(InstalledApplication, name='clusters')
class ClusterAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= Cluster
    table = ClusterTableApplication
    template_name = "adestis_netbox_applications/cluster.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        # 'bulk_import': {'add'},
        # # 'bulk_edit': {'change'},
        'bulk_remove_cluster': {'change'},
    }

    tab = ViewTab(
        label=_('Clusters'),
        badge=lambda obj: obj.cluster.count(),
        weight=600
    )

    def get_children(self, request, parent):
        return Cluster.objects.restrict(request.user, 'view').filter(installedapplication=parent)
 
@register_model_view(Cluster, name='applications')
class ClusterAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = Cluster.objects.all()
    child_model= InstalledApplication
    table = InstalledApplicationTableTab
    template_name = "adestis_netbox_applications/application_cluster.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        # 'bulk_import': {'add'},
        # 'bulk_edit': {'change'},
        'bulk_remove_installedapplication': {'change'},
    }

    tab = ViewTab(
        label=_('Applications'),
        badge=lambda obj: obj.installedapplication.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return InstalledApplication.objects.restrict(request.user, 'view').filter(cluster=parent)
    
@register_model_view(InstalledApplication, 'assign_cluster')
class InstalledApplicationAssignCluster(generic.ObjectEditView):
    queryset = InstalledApplication.objects.prefetch_related(
        'cluster', 'tags', 
    ).all()
    
    form = InstalledApplicationAssignClusterForm
    template_name = 'adestis_netbox_applications/assign_cluster.html'

    def get(self, request, pk):
        installedapplication = get_object_or_404(self.queryset, pk=pk)
        form = self.form(installedapplication,  initial=request.GET)

        return render(request, self.template_name, {
            'installedapplication': installedapplication,
            'form': form,
            'return_url': reverse('plugins:adestis_netbox_applications:installedapplication', kwargs={'pk': pk}),
            'edit_url': reverse('plugins:adestis_netbox_applications:installedapplication_assign_cluster', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        installedapplication = get_object_or_404(self.queryset, pk=pk)
        form = self.form(installedapplication, request.POST)

        if form.is_valid():
            
            selected_cluster_groups = form.cleaned_data['cluster_group']
            selected_clusters = form.cleaned_data['cluster']
            with transaction.atomic():
                
                for cluster in Cluster.objects.filter(pk__in=selected_clusters): 
                    installedapplication.cluster.add(cluster)
                    
                for cluster_group in ClusterGroup.objects.filter(pk__in=selected_cluster_groups): 
                    installedapplication.cluster_group.add(cluster_group)
            
            installedapplication.save()
            
            return redirect(installedapplication.get_absolute_url())

        return render(request, self.template_name, {
            'installedapplication': installedapplication,
            'form': form,
            'return_url': installedapplication.get_absolute_url(),
            'edit_url': reverse('plugins:adestis_netbox_applications:installedapplication_assign_cluster', kwargs={'pk': pk}),
        })
        
@register_model_view(InstalledApplication, 'remove_cluster', path='cluster/remove')
class InstalledApplicationRemoveClusterView(generic.ObjectEditView):
    queryset = InstalledApplication.objects.all()
    form = InstalledApplicationRemoveCluster
    template_name = 'generic/bulk_remove.html'

    def post(self, request, pk):

        installedapplication = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            
            form = self.form(request.POST)
            if form.is_valid():
                
                cluster_pks = form.cleaned_data['pk']
                with transaction.atomic(): 
                    installedapplication.cluster.remove(*cluster_pks)
                    installedapplication.save()

                messages.success(request, _("Removed {count} clusters from applications {installedapplication}").format(
                    count=len(cluster_pks),
                    installedapplication=installedapplication
                ))
                return redirect(installedapplication.get_absolute_url())
        else:
            form = self.form(initial={'pk': request.POST.getlist('pk')})

        selected_objects = Cluster.objects.filter(pk__in=form.initial['pk'])
        cluster_table = ClusterTable(list(selected_objects), orderable=False)
        cluster_table.configure(request)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': installedapplication,
            'table': cluster_table,
            'obj_type_plural': 'clusters',
            'return_url': installedapplication.get_absolute_url(),
        })
    
    
@register_model_view(InstalledApplication, name='cluster groups')
class ClusterGroupAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= ClusterGroup
    table = ClusterGroupTableApplication
    template_name = "adestis_netbox_applications/cluster_group.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        # 'bulk_import': {'add'},
        # 'bulk_edit': {'change'},
        'bulk_remove_cluster_group': {'change'},
    }

    tab = ViewTab(
        label=_('Cluster Groups'),
        badge=lambda obj: obj.cluster_group.count(),
        weight=600
    )

    def get_children(self, request, parent):
        return ClusterGroup.objects.restrict(request.user, 'view').filter(installedapplication=parent)

@register_model_view(ClusterGroup, name='applications')
class ClusterGroupAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = ClusterGroup.objects.all()
    child_model= InstalledApplication
    table = InstalledApplicationTableTab
    template_name = "adestis_netbox_applications/application_clustergroup.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        # 'bulk_import': {'add'},
        # 'bulk_edit': {'change'},
        'bulk_remove_installedapplication': {'change'},
    }

    tab = ViewTab(
        label=_('Applications'),
        badge=lambda obj: obj.installedapplication.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return InstalledApplication.objects.restrict(request.user, 'view').filter(cluster_group=parent)
    
    
@register_model_view(InstalledApplication, 'assign_cluster_group')
class InstalledApplicationAssignClusterGroup(generic.ObjectEditView):
    queryset = InstalledApplication.objects.prefetch_related(
        'cluster_group', 'tags', 
    ).all()
    
    form = InstalledApplicationAssignClusterGroupForm
    template_name = 'adestis_netbox_applications/assign_cluster_group.html'

    def get(self, request, pk):
        installedapplication = get_object_or_404(self.queryset, pk=pk)
        form = self.form(installedapplication,  initial=request.GET)

        return render(request, self.template_name, {
            'installedapplication': installedapplication,
            'form': form,
            'return_url': reverse('plugins:adestis_netbox_applications:installedapplication', kwargs={'pk': pk}),
            'edit_url': reverse('plugins:adestis_netbox_applications:installedapplication_assign_cluster_group', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        installedapplication = get_object_or_404(self.queryset, pk=pk)
        form = self.form(installedapplication, request.POST)

        if form.is_valid():
            
            selected_cluster_groups = form.cleaned_data['cluster_group']
            with transaction.atomic():
                
                for cluster_group in ClusterGroup.objects.filter(pk__in=selected_cluster_groups): 
                    installedapplication.cluster_group.add(cluster_group)
            
            installedapplication.save()
            
            return redirect(installedapplication.get_absolute_url())

        return render(request, self.template_name, {
            'installedapplication': installedapplication,
            'form': form,
            'return_url': installedapplication.get_absolute_url(),
            'edit_url': reverse('plugins:adestis_netbox_applications:installedapplication_assign_cluster_group', kwargs={'pk': pk}),
        })
        
@register_model_view(InstalledApplication, 'remove_cluster_group', path='clustergroup/remove')
class InstalledApplicationRemoveClusterGroupView(generic.ObjectEditView):
    queryset = InstalledApplication.objects.all()
    form = InstalledApplicationRemoveClusterGroup
    template_name = 'generic/bulk_remove.html'

    def post(self, request, pk):

        installedapplication = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            
            form = self.form(request.POST)
            if form.is_valid():
                
                clustergroup_pks = form.cleaned_data['pk']
                with transaction.atomic():
                    installedapplication.cluster_group.remove(*clustergroup_pks)
                    installedapplication.save()

                messages.success(request, _("Removed {count} cluster groups from applications {installedapplication}").format(
                    count=len(clustergroup_pks),
                    installedapplication=installedapplication
                ))
                return redirect(installedapplication.get_absolute_url())
        else:
            form = self.form(initial={'pk': request.POST.getlist('pk')})

        selected_objects = ClusterGroup.objects.filter(pk__in=form.initial['pk'])
        cluster_group_table = ClusterGroupTable(list(selected_objects), orderable=False)
        cluster_group_table.configure(request)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': installedapplication,
            'table': cluster_group_table,
            'obj_type_plural': 'cluster groups',
            'return_url': installedapplication.get_absolute_url(),
        })


@register_model_view(InstalledApplication, name='virtual machines')
class VirtualMachineAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= VirtualMachine
    table = VirtualMachineTableApplication
    template_name = "adestis_netbox_applications/virtual_machine.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        # 'bulk_import': {'add'},
        # 'bulk_edit': {'change'},
        'bulk_remove_virtual_machine': {'change'},
    }

    tab = ViewTab(
        label=_('Virtual Machines'),
        badge=lambda obj: obj.virtual_machine.count(),
        weight=600
    )

    def get_children(self, request, parent):
        return VirtualMachine.objects.restrict(request.user, 'view').filter(installedapplication=parent)
  
@register_model_view(VirtualMachine, name='applications')
class VirtualMachineAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = VirtualMachine.objects.all()
    child_model= InstalledApplication
    table = InstalledApplicationTableTab
    template_name = "adestis_netbox_applications/application_virtualmachine.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        # 'bulk_import': {'add'},
        # 'bulk_edit': {'change'},
        'bulk_remove_installedapplication': {'change'},
    }

    tab = ViewTab(
        label=_('Applications'),
        badge=lambda obj: obj.installedapplication.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return InstalledApplication.objects.restrict(request.user, 'view').filter(virtual_machine=parent)
    
    
@register_model_view(InstalledApplication, 'assign_virtual_machine')
class InstalledApplicationAssignVirtualMachine(generic.ObjectEditView):
    queryset = InstalledApplication.objects.prefetch_related(
        'virtual_machine', 'tags', 
    ).all()
    
    form = InstalledApplicationAssignVirtualMachineForm
    template_name = 'adestis_netbox_applications/assign_virtual_machine.html'

    def get(self, request, pk):
        installedapplication = get_object_or_404(self.queryset, pk=pk)
        form = self.form(installedapplication,  initial=request.GET)

        return render(request, self.template_name, {
            'installedapplication': installedapplication,
            'form': form,
            'return_url': reverse('plugins:adestis_netbox_applications:installedapplication', kwargs={'pk': pk}),
            'edit_url': reverse('plugins:adestis_netbox_applications:installedapplication_assign_virtual_machine', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        installedapplication = get_object_or_404(self.queryset, pk=pk)
        form = self.form(installedapplication, request.POST)

        if form.is_valid():
            
            selected_vm = form.cleaned_data['virtual_machine']
            with transaction.atomic():
                
                for virtual_machine in VirtualMachine.objects.filter(pk__in=selected_vm): 
                    installedapplication.virtual_machine.add(virtual_machine)
            
            installedapplication.save()
            
            return redirect(installedapplication.get_absolute_url())

        return render(request, self.template_name, {
            'installedapplication': installedapplication,
            'form': form,
            'return_url': installedapplication.get_absolute_url(),
            'edit_url': reverse('plugins:adestis_netbox_applications:installedapplication_assign_virtual_machine', kwargs={'pk': pk}),
        })
        
@register_model_view(InstalledApplication, 'remove_virtual_machine', path='virtualmachine/remove')
class InstalledApplicationRemoveVirtualMachineView(generic.ObjectEditView):
    queryset = InstalledApplication.objects.all()
    form = InstalledApplicationRemoveVirtualMachine
    template_name = 'generic/bulk_remove.html'

    def post(self, request, pk):

        installedapplication = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            
            form = self.form(request.POST)
            if form.is_valid():
                
                virtualmachine_pks = form.cleaned_data['pk']
                with transaction.atomic():
                    installedapplication.virtual_machine.remove(*virtualmachine_pks)
                    installedapplication.save()

                messages.success(request, _("Removed {count} virtual machines from applications {installedapplication}").format(
                    count=len(virtualmachine_pks),
                    installedapplication=installedapplication
                ))
                return redirect(installedapplication.get_absolute_url())
        else:
            form = self.form(initial={'pk': request.POST.getlist('pk')})

        selected_objects = VirtualMachine.objects.filter(pk__in=form.initial['pk'])
        virtual_machine_table = VirtualMachineTable(list(selected_objects), orderable=False)
        virtual_machine_table.configure(request)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': installedapplication,
            'table': virtual_machine_table,
            'obj_type_plural': 'virtual machines',
            'return_url': installedapplication.get_absolute_url(),
        })