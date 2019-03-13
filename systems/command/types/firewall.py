from settings.roles import Roles
from .network import NetworkRouterCommand, NetworkActionCommand


class FirewallRouterCommand(NetworkRouterCommand):

    def get_priority(self):
        return 50


class FirewallActionCommand(NetworkActionCommand):

    def get_priority(self):
        return 50

    def groups_allowed(self):
        return super().groups_allowed() + [
            Roles.security_admin
        ]

