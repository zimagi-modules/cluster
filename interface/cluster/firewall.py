from systems.command.base import command_list
from systems.command.factory import resource, router
from systems.command.types import firewall


class Command(firewall.FirewallRouterCommand):

    def get_subcommands(self):
        network_provider_name = 'network'
        firewall_rule_name = 'firewall_rule'

        return command_list(
            resource.ResourceCommandSet(
                firewall.FirewallActionCommand, self.name,
                provider_name = network_provider_name,
                provider_subtype = self.name
            ),
            ('rule', router.Router(
                firewall.FirewallRouterCommand,
                resource.ResourceCommandSet(
                    firewall.FirewallActionCommand, firewall_rule_name,
                    provider_name = network_provider_name,
                    provider_subtype = firewall_rule_name
                )
            ))
        )
