from django.db import models as django

from systems.models import network, group, provider


class SubnetFacade(
    provider.ProviderModelFacadeMixin,
    group.GroupModelFacadeMixin,
    network.NetworkModelFacadeMixin
):
    def get_field_cidr_display(self, instance, value, short):
        return value

    def get_field_nat_subnets_display(self, instance, value, short):
        subnets = [ str(x) for x in value.all() ]
        return "\n".join(subnets)


class Subnet(
    provider.ProviderMixin,
    group.GroupMixin,
    network.NetworkModel
):
    cidr = django.CharField(null = True, max_length = 128)

    use_public_ip = django.BooleanField(default = True)
    use_nat = django.BooleanField(default = False)

    nat_subnet = django.ForeignKey("Subnet",
        null = True,
        on_delete = django.SET_NULL,
        related_name = "%(class)s_relation",
        editable = False
    )

    class Meta(network.NetworkModel.Meta):
        verbose_name = "subnet"
        verbose_name_plural = "subnets"
        facade_class = SubnetFacade
        relation = ['nat_subnet']
        ordering = ['cidr']
        provider_name = 'network:subnet'
        provider_relation = 'network'

    def __str__(self):
        return "{} ({})".format(self.name, self.cidr)
