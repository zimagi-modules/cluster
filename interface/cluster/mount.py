from systems.command.factory import resource
from systems.command.types import mount


class Command(mount.MountRouterCommand):

    def get_subcommands(self):
        return resource.ResourceCommandSet(
            mount.MountActionCommand, self.name,
            provider_name = 'storage',
            provider_subtype = self.name
        )
