from django.conf import settings

from systems.command.providers import meta, terraform


class StorageProvider(terraform.TerraformProvider):

    def terraform_type(self):
        return 'storage'

    @property
    def facade(self):
        return self.command._storage


class StorageMountProvider(terraform.TerraformProvider):

    def provider_config(self, type = None):
        self.option(str, 'mount_options', 'nfs4 rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 0 0', help = 'Mount options', config_name = 'manual_mount_options')

    def terraform_type(self):
        return 'storage_mount'

    @property
    def facade(self):
        return self.command._mount


class BaseStorageProvider(meta.MetaCommandProvider):

    def __init__(self, name, command, instance = None):
        super().__init__(name, command, instance)
        self.provider_type = 'storage'
        self.provider_options = settings.STORAGE_PROVIDERS

    def register_types(self):
        self.set('storage', StorageProvider)
        self.set('mount', StorageMountProvider)
