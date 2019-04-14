from django.db import models as django

from data.network.models import Network
from systems.models import network_peering, provider


class NetworkPeeringRelationFacade(
    provider.ProviderModelFacadeMixin,
    network_peering.NetworkPeeringModelFacadeMixin
):
    pass


class NetworkPeeringRelation(
    provider.ProviderMixin,
    network_peering.NetworkPeeringModel
):
    network1 = django.ForeignKey(Network,
        null = True,
        on_delete = django.PROTECT,
        related_name = "%(class)s_relation1",
        editable = False
    )
    network2 = django.ForeignKey(Network,
        null = True,
        on_delete = django.PROTECT,
        related_name = "%(class)s_relation2",
        editable = False
    )

    class Meta(network_peering.NetworkPeeringModel.Meta):
        verbose_name = "network peering relation"
        verbose_name_plural = "network peering relations"
        facade_class = NetworkPeeringRelationFacade
        relation = ['network1', 'network2']
        provider_name = 'network_peering:network_relation'
        provider_relation = 'network_peering'
        command_base = False

    def __str__(self):
        return "{}".format(self.name)
