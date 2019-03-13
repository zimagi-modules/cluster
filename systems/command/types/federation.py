from settings.roles import Roles
from .router import RouterCommand
from .action import ActionCommand
from systems.command.mixins import network, federation


class FederationRouterCommand(RouterCommand):

    def get_priority(self):
        return 65


class FederationActionCommand(
    network.NetworkMixin,
    federation.FederationMixin,
    ActionCommand
):
    def groups_allowed(self):
        return [
            Roles.admin,
            Roles.network_admin
        ]

    def server_enabled(self):
        return True

    def get_priority(self):
        return 65
