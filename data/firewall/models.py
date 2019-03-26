from django.db import models as django

from systems.models import group, network, provider


class FirewallFacade(
    provider.ProviderModelFacadeMixin,
    group.GroupModelFacadeMixin,
    network.NetworkModelFacadeMixin
):
    pass


class Firewall(
    provider.ProviderMixin,
    group.GroupMixin,
    network.NetworkModel
):
    class Meta(network.NetworkModel.Meta):
        verbose_name = "firewall"
        verbose_name_plural = "firewalls"
        facade_class = FirewallFacade
        ordering = ['name']
        provider_name = 'network:firewall'
        provider_relation = 'network'

    def __str__(self):
        return "{}".format(self.name)
