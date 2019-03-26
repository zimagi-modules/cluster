from systems.command.factory import resource
from systems.command.types import storage


class Command(storage.StorageRouterCommand):

    def get_subcommands(self):
        return resource.ResourceCommandSet(
            storage.StorageActionCommand, self.name,
            provider_name = self.name,
            provider_subtype = self.name
        )
