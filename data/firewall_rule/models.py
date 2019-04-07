from django.db import models as django

from systems.models import base, fields, firewall, provider


class FirewallRuleFacade(
    provider.ProviderModelFacadeMixin,
    firewall.FirewallModelFacadeMixin
):
    def get_field_cidrs_display(self, instance, value, short):
        return "\n".join(value)


class FirewallRule(
    provider.ProviderMixin,
    firewall.FirewallRelationMixin,
    firewall.FirewallModel
):
    mode = django.CharField(
        max_length = 10,
        default = 'ingress',
        choices = base.format_choices('ingress', 'egress'),
    )
    protocol = django.CharField(
        max_length = 10,
        default = 'tcp',
        choices = base.format_choices('tcp', 'udp', 'icmp')
    )
    from_port = django.IntegerField(null = True)
    to_port = django.IntegerField(null = True)
    cidrs = fields.CSVField(null = True)

    class Meta(firewall.FirewallModel.Meta):
        verbose_name = "firewall rule"
        verbose_name_plural = "firewall rules"
        facade_class = FirewallRuleFacade
        ordering = ['name']
        provider_name = 'network:firewall_rule'
        provider_relation = 'firewall'

    def __str__(self):
        return "{}".format(self.name)
