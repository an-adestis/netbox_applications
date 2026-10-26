try:
    from netbox.object_actions import (
        AddObject,
        BulkDelete,
        BulkEdit,
        BulkExport,
        BulkImport,
        ObjectAction,
    )
except ImportError:
    class ObjectAction:
        name = ''
        permissions_required = set()
        multi = False

    class AddObject(ObjectAction):
        name = 'add'
        permissions_required = {'add'}

    class BulkDelete(ObjectAction):
        name = 'bulk_delete'
        permissions_required = {'delete'}
        multi = True

    class BulkEdit(ObjectAction):
        name = 'bulk_edit'
        permissions_required = {'change'}
        multi = True

    class BulkExport(ObjectAction):
        name = 'export'
        permissions_required = {'view'}
        multi = True

    class BulkImport(ObjectAction):
        name = 'bulk_import'
        permissions_required = {'add'}


try:
    from netbox.object_actions import ObjectAction as NetBoxObjectAction
except ImportError:
    NetBoxObjectAction = None


def actions(*action_classes):
    if NetBoxObjectAction is not None:
        return action_classes
    return {
        action.name: action.permissions_required
        for action in action_classes
    }


class PermissionOnlyBulkAction(ObjectAction):
    multi = True

    if NetBoxObjectAction is not None:
        @classmethod
        def render(cls, context, obj, **kwargs):
            return ''


class BulkRemoveSoftwareVersions(PermissionOnlyBulkAction):
    name = 'bulk_remove_software_versions'
    permissions_required = {'remove'}


class BulkRemoveCertificate(PermissionOnlyBulkAction):
    name = 'bulk_remove_certificate'
    permissions_required = {'change'}


class BulkRemoveDevice(PermissionOnlyBulkAction):
    name = 'bulk_remove_device'
    permissions_required = {'change'}


class BulkRemoveInstalledApplication(PermissionOnlyBulkAction):
    name = 'bulk_remove_installedapplication'
    permissions_required = {'change'}


class BulkRemoveCluster(PermissionOnlyBulkAction):
    name = 'bulk_remove_cluster'
    permissions_required = {'change'}


class BulkRemoveClusterGroup(PermissionOnlyBulkAction):
    name = 'bulk_remove_cluster_group'
    permissions_required = {'change'}


class BulkRemoveVirtualMachine(PermissionOnlyBulkAction):
    name = 'bulk_remove_virtual_machine'
    permissions_required = {'change'}


class BulkRemoveContact(PermissionOnlyBulkAction):
    name = 'bulk_remove_contact'
    permissions_required = {'change'}


class BulkRemoveSoftware(PermissionOnlyBulkAction):
    name = 'bulk_remove_software'
    permissions_required = {'change'}
