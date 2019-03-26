from systems.command.factory import resource
from systems.command.types import federation


class Command(federation.FederationRouterCommand):

    def get_subcommands(self):
        return resource.ResourceCommandSet(
            federation.FederationActionCommand, self.name
        )
