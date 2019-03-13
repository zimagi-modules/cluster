from systems.command.base import command_list
from systems.command.factory import resource
from systems.command.types import mount


class Command(mount.MountRouterCommand):

    def get_command_name(self):
        return 'mount'

    def get_subcommands(self):
        base_name = self.get_command_name()
        return resource.ResourceCommandSet(
            mount.MountActionCommand, base_name,
            provider_name = 'storage',
            provider_subtype = base_name
        )
