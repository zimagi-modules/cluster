from django.db import models as django

from data.network_peering.models import NetworkPeering
from .resource import ResourceModel, ResourceModelFacadeMixin


class NetworkPeeringModelFacadeMixin(ResourceModelFacadeMixin):

    def get_field_network_peering_display(self, instance, value, short):
        return str(value)

    def get_field_network_peerings_display(self, instance, value, short):
        network_peerings = [ str(x) for x in value.all() ]
        return "\n".join(network_peerings)


class NetworkPeeringMixin(django.Model):

    network_peering = django.ForeignKey(NetworkPeering,
        null = True,
        on_delete = django.PROTECT,
        related_name = "%(class)s_relation",
        editable = False
    )
    class Meta:
        abstract = True

class NetworkPeeringRelationMixin(django.Model):

    network_peerings = django.ManyToManyField(NetworkPeering,
        related_name = "%(class)s_relations",
        editable = False
    )
    class Meta:
        abstract = True


class NetworkPeeringModel(NetworkPeeringMixin, ResourceModel):

    class Meta(ResourceModel.Meta):
        abstract = True
        unique_together = ('network_peering', 'name')
        scope = 'network_peering'

    def __str__(self):
        return "{}:{}".format(self.network_peering.name, self.name)

    def get_id_fields(self):
        return ('name', 'network_peering_id')
