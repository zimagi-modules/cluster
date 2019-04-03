from settings.roles import Roles
from .router import RouterCommand
from .action import ActionCommand
from systems.command.mixins import domain


class DomainRouterCommand(RouterCommand):

    def get_priority(self):
        return 65


class DomainActionCommand(
    domain.DomainMixin,
    ActionCommand
):
    def get_priority(self):
        return 65

    def server_enabled(self):
        return True

    def groups_allowed(self):
        return [
            Roles.admin,
            Roles.network_admin,
            Roles.security_admin
        ]

