from django.db import models as django

from systems.models import network, group, firewall, provider


class LoadBalancerFacade(
    provider.ProviderModelFacadeMixin,
    group.GroupModelFacadeMixin,
    firewall.FirewallModelFacadeMixin,
    network.NetworkModelFacadeMixin
):
    def get_field_internal_display(self, instance, value, short):
        return str(value)


class LoadBalancer(
    provider.ProviderMixin,
    group.GroupMixin,
    firewall.FirewallRelationMixin,
    network.NetworkModel
):
    internal = django.BooleanField(default = False)

    class Meta(network.NetworkModel.Meta):
        verbose_name = "load_balancer"
        verbose_name_plural = "load_balancers"
        facade_class = LoadBalancerFacade
        provider_name = 'load_balancer'

    def __str__(self):
        return "{}".format(self.name)
