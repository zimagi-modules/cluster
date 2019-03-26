from django.db import models as django

from systems.models import network, group, provider


class SubnetFacade(
    provider.ProviderModelFacadeMixin,
    group.GroupModelFacadeMixin,
    network.NetworkModelFacadeMixin
):
    def get_list_fields(self):
        return (
            ('name', 'Name'),
            ('network', 'Network'),
            ('type', 'Type'),
            ('cidr', 'CIDR'),
            ('config', 'Configuration'),
            ('variables', 'Resources')
        )

    def get_display_fields(self):
        return (
            ('name', 'Name'),
            ('network', 'Network'),
            ('type', 'Type'),
            ('cidr', 'CIDR'),
            '---',
            ('config', 'Configuration'),
            '---',
            ('variables', 'Resources'),
            ('state_config', 'State'),
            '---',
            ('created', 'Created'),
            ('updated', 'Updated')
        )

    def get_field_cidr_display(self, instance, value, short):
        return value


class Subnet(
    provider.ProviderMixin,
    group.GroupMixin,
    network.NetworkModel
):
    cidr = django.CharField(null=True, max_length=128)

    class Meta(network.NetworkModel.Meta):
        verbose_name = "subnet"
        verbose_name_plural = "subnets"
        facade_class = SubnetFacade
        ordering = ['cidr']
        provider_name = 'network:subnet'
        provider_relation = 'network'

    def __str__(self):
        return "{} ({})".format(self.name, self.cidr)
