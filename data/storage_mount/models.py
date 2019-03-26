from django.db import models as django

from systems.models import subnet, storage, firewall, provider


class StorageMountFacade(
    provider.ProviderModelFacadeMixin,
    firewall.FirewallModelFacadeMixin,
    subnet.SubnetModelFacadeMixin,
    storage.StorageModelFacadeMixin
):
    def get_list_fields(self):
        return (
            ('name', 'Name'),
            ('subnet', 'Subnet'),
            ('storage', 'Storage'),
            ('type', 'Type'),
            ('remote_host', 'Remote host'),
            ('remote_path', 'Remote path'),
        )

    def get_display_fields(self):
        return (
            ('name', 'Name'),
            ('subnet', 'Subnet'),
            ('storage', 'Storage'),
            ('type', 'Type'),
            '---',
            ('remote_host', 'Remote host'),
            ('remote_path', 'Remote path'),
            ('mount_options', 'Mount options'),
            '---',
            ('config', 'Configuration'),
            '---',
            ('variables', 'Variables'),
            ('state_config', 'State'),
            '---',
            ('created', 'Created'),
            ('updated', 'Updated')
        )

    def get_field_remote_host_display(self, instance, value, short):
        return value

    def get_field_remote_path_display(self, instance, value, short):
        return value

    def get_field_mount_options_display(self, instance, value, short):
        return value


class StorageMount(
    provider.ProviderMixin,
    firewall.FirewallRelationMixin,
    subnet.SubnetMixin,
    storage.StorageModel
):
    remote_host = django.CharField(null=True, max_length=128)
    remote_path = django.CharField(null=True, max_length=256)
    mount_options = django.TextField(null=True)

    class Meta(storage.StorageModel.Meta):
        verbose_name = "mount"
        verbose_name_plural = "mounts"
        facade_class = StorageMountFacade
        unique_together = (
            ('storage', 'name'),
            ('subnet', 'name')
        )
        scope = ('storage', 'subnet')
        ordering = ['name']
        provider_name = 'storage:mount'
        provider_relation = 'storage'

    def __str__(self):
        return "{} ({}:{})".format(self.name, self.remote_host, self.remote_path)

    def get_id_fields(self):
        return ('name', 'storage_id', 'subnet_id')
