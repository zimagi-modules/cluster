from settings.roles import Roles
from .router import RouterCommand
from .action import ActionCommand
from systems.command.mixins import network, storage, server


class NetworkRouterCommand(RouterCommand):

    def get_priority(self):
        return 60


class NetworkActionCommand(
    server.ServerMixin,
    storage.StorageMixin,
    network.NetworkMixin,
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
        return 60
