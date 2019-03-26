from django.db import models as django

from systems.models import group, network, provider


class FirewallFacade(
    provider.ProviderModelFacadeMixin,
    group.GroupModelFacadeMixin,
    network.NetworkModelFacadeMixin
):
    def get_relations(self):
        return {
            'groups': ('group', 'Groups', '--groups'),
            'firewallrule_relation': ('firewall_rule', 'Rules')
        }

    def get_list_fields(self):
        return (
            ('name', 'Name'),
            ('network', 'Network'),
            ('type', 'Type'),
            ('config', 'Configuration'),
            ('variables', 'Resources')
        )

    def get_display_fields(self):
        return (
            ('name', 'Name'),
            ('network', 'Network'),
            ('type', 'Type'),
            '---',
            ('config', 'Configuration'),
            '---',
            ('variables', 'Resources'),
            ('state_config', 'State'),
            '---',
            ('created', 'Created'),
            ('updated', 'Updated')
        )


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
