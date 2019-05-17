from django.db import models as django

from systems.models import subnet, storage, firewall, provider


class StorageMountFacade(
    provider.ProviderModelFacadeMixin,
    firewall.FirewallModelFacadeMixin,
    storage.StorageModelFacadeMixin,
    subnet.SubnetModelFacadeMixin
):
    def get_field_remote_host_display(self, instance, value, short):
        return value

    def get_field_remote_path_display(self, instance, value, short):
        return value

    def get_field_mount_options_display(self, instance, value, short):
        return value


class StorageMount(
    provider.ProviderMixin,
    firewall.FirewallRelationMixin,
    storage.StorageMixin,
    subnet.SubnetModel
):
    remote_host = django.CharField(null = True, max_length = 128)
    remote_path = django.CharField(null = True, max_length = 256)
    mount_options = django.TextField(null = True)

    class Meta(subnet.SubnetModel.Meta):
        verbose_name = "mount"
        verbose_name_plural = "mounts"
        facade_class = StorageMountFacade
        scope = ('storage', 'subnet')
        ordering = ['name']
        provider_name = 'storage:mount'
        provider_relation = 'storage'

    def __str__(self):
        return "{} ({}:{})".format(self.name, self.remote_host, self.remote_path)

    def get_id_fields(self):
        return ('name', 'storage_id', 'subnet_id')
