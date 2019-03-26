from django.db import models as django

from systems.models import group, network, provider


class StorageFacade(
    provider.ProviderModelFacadeMixin,
    group.GroupModelFacadeMixin,
    network.NetworkModelFacadeMixin
):
    pass


class Storage(
    provider.ProviderMixin,
    group.GroupMixin,
    network.NetworkModel
):
    class Meta(network.NetworkModel.Meta):
        verbose_name = "storage"
        verbose_name_plural = "storage"
        facade_class = StorageFacade
        ordering = ['name']
        provider_name = 'storage:storage'

    def __str__(self):
        return "{}".format(self.name)
