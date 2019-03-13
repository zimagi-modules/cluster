from systems.command.base import command_list
from systems.command.factory import resource
from systems.command.types import subnet


class Command(subnet.SubnetRouterCommand):

    def get_command_name(self):
        return 'subnet'

    def get_subcommands(self):
        base_name = self.get_command_name()
        return resource.ResourceCommandSet(
            subnet.SubnetActionCommand, base_name,
            provider_name = 'network',
            provider_subtype = base_name
        )
