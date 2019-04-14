from django.db import models as django

from systems.models import environment, network, provider


class NetworkPeeringFacade(
    provider.ProviderModelFacadeMixin,
    network.NetworkModelFacadeMixin,
    environment.EnvironmentModelFacadeMixin
):
    pass


class NetworkPeering(
    provider.ProviderMixin,
    network.NetworkRelationMixin,
    environment.EnvironmentModel
):
    class Meta(environment.EnvironmentModel.Meta):
        verbose_name = "network peering"
        verbose_name_plural = "network peerings"
        facade_class = NetworkPeeringFacade
        provider_name = 'network_peering:network_peering'

    def __str__(self):
        return "{}".format(self.name)
