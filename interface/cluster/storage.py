from systems.command.base import command_list
from systems.command.factory import resource
from systems.command.types import storage


class Command(storage.StorageRouterCommand):

    def get_command_name(self):
        return 'storage'

    def get_subcommands(self):
        base_name = self.get_command_name()
        return resource.ResourceCommandSet(
            storage.StorageActionCommand, base_name,
            provider_name = base_name,
            provider_subtype = base_name
        )
