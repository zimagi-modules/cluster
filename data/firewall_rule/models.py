from django.db import models as django

from systems.models import fields, firewall, provider


class FirewallRuleFacade(
    provider.ProviderModelFacadeMixin,
    firewall.FirewallModelFacadeMixin
):
    def get_field_network_display(self, instance, value, short):
        return str(instance.firewall.network)

    def get_field_mode_display(self, instance, value, short):
        return value

    def get_field_protocol_display(self, instance, value, short):
        return value

    def get_field_from_port_display(self, instance, value, short):
        return str(value)

    def get_field_to_port_display(self, instance, value, short):
        return str(value)

    def get_field_cidrs_display(self, instance, value, short):
        return "\n".join(value)


class FirewallRule(
    provider.ProviderMixin,
    firewall.FirewallModel
):
    mode = django.CharField(max_length=10, default='ingress', choices=[(i, i) for i in ('ingress', 'egress')])
    from_port = django.IntegerField(null=True)
    to_port = django.IntegerField(null=True)
    protocol = django.CharField(max_length=10, default='tcp', choices=[(i, i) for i in ('tcp', 'udp', 'icmp')])
    cidrs = fields.CSVField(null=True)

    class Meta(firewall.FirewallModel.Meta):
        verbose_name = "firewall rule"
        verbose_name_plural = "firewall rules"
        facade_class = FirewallRuleFacade
        ordering = ['name']
        provider_name = 'network:firewall_rule'
        provider_relation = 'firewall'

    def __str__(self):
        return "{}".format(self.name)
